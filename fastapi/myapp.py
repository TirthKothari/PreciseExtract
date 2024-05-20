from fastapi import FastAPI,UploadFile,File,Header
from typing import List,Annotated
import shutil,os
from werkzeug.utils import secure_filename
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
import jwt
from jose import jwe
from pdf2image import convert_from_path
import json
import mysql.connector
from bs4 import BeautifulSoup
# from transformers import AutoModelForObjectDetection
# import torch
# from PIL import Image
# from huggingface_hub import hf_hub_download
# from torchvision import transforms
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from matplotlib.patches import Patch
from paddleocr import PPStructure,draw_structure_result,save_structure_res
import cv2
from pathlib import Path
from dateutil import parser
from datetime import datetime

mydb = mysql.connector.connect(
    host='localhost',
    user='tirth',
    password = 'tirth123',
    database='precise_extract'
)

mycursor = mydb.cursor()


class Settings(BaseSettings):
    SECRET_KEY:str = '8a27dc7b112ed8e70ca02fa3778e04b6'
    AES_SECRET_KEY :bytes = b'1!\x14\xd8?\x03\xefm\xa0*1\xaf\xd8\xe7\x9b\xdcb\xed\xeek\xf8?\\:@\xed,\x06*\xcbYL'

settings = Settings()
app = FastAPI()

origins = [
    "http://127.0.0.1:5000",
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:5000",
    "http://10.110.7.91:5000",
    "http://10.110.7.91:8000",
    "http://192.168.236.93:5000",
    "http://192.168.236.93:8000",
    "http://192.168.0.104:5000",
    "http://10.110.12.229:5000",
    "http://192.168.0.104:5000",
    "http://192.168.0.104:8000",
    "http://192.168.211.93:5000",
    "http://192.168.211.93:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

######################################## PDF2IMAGE ##############################
def pdf2images(path):
    dir = os.listdir(path)
    with open(os.path.join(path,"status.json"),'r') as f:
        status = json.load(f)
        f.close()
    with open(os.path.join(path,"status.json"),'w') as f:
        for d in dir:
                filename , filextention = os.path.splitext(d)
                if filextention == '.pdf' or filextention == '.PDF':
                    print(os.path.join(path,d))
                    images = convert_from_path(os.path.join(path,d),80)
                    for i in range(len(images)):
                        print([item["filename"] for item in status])
                        print("pdf")
                        print(f"{filename}{i}.jpg")
                        if f"{filename}{i}.jpg" not in [item["filename"] for item in status]:
                            images[i].save(os.path.join(path,f'{filename}'+ str(i)+'.jpg'),"JPEG")
                            status.append({"filename":f'{filename}'+ str(i)+'.jpg',"status":False})
                    if os.path.isfile(os.path.join(path,d)):
                        os.remove(os.path.join(path,d))
                elif filextention.casefold() in ['.jpeg','.jpg','.png']:
                    print([item["filename"] for item in status])
                    print("image")
                    print(f"{filename}{filextention}")
                    if f"{filename}{filextention}" not in [item["filename"] for item in status]:
                        print("changed")
                        status.append({"filename":f'{filename}{filextention}',"status":False})
        json.dump(status,f)
        f.close()
    
######################################## PDF2IMAGE END ##############################

####################################### Extraction #################################

class MaxResize(object):
    def __init__(self, max_size=800):
        self.max_size = max_size

    def __call__(self, image):
        width, height = image.size
        current_max_size = max(width, height)
        scale = self.max_size / current_max_size
        resized_image = image.resize((int(round(scale*width)), int(round(scale*height))))

        return resized_image
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(-1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h), (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)
def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b   
def outputs_to_objects(outputs, img_size, id2label):
    m = outputs.logits.softmax(-1).max(-1)
    pred_labels = list(m.indices.detach().cpu().numpy())[0]
    pred_scores = list(m.values.detach().cpu().numpy())[0]
    pred_bboxes = outputs['pred_boxes'].detach().cpu()[0]
    pred_bboxes = [elem.tolist() for elem in rescale_bboxes(pred_bboxes, img_size)]

    objects = []
    for label, score, bbox in zip(pred_labels, pred_scores, pred_bboxes):
        class_label = id2label[int(label)]
        if not class_label == 'no object':
            objects.append({'label': class_label, 'score': float(score),
                            'bbox': [float(elem) for elem in bbox]})

    return objects
def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img
def visualize_detected_tables(img, det_tables, out_path=None):
    plt.imshow(img, interpolation="lanczos")
    fig = plt.gcf()
    fig.set_size_inches(20, 20)
    ax = plt.gca()

    for det_table in det_tables:
        bbox = det_table['bbox']

        if det_table['label'] == 'table':
            facecolor = (1, 0, 0.45)
            edgecolor = (1, 0, 0.45)
            alpha = 0.3
            linewidth = 2
            hatch='//////'
        elif det_table['label'] == 'table rotated':
            facecolor = (0.95, 0.6, 0.1)
            edgecolor = (0.95, 0.6, 0.1)
            alpha = 0.3
            linewidth = 2
            hatch='//////'
        else:
            continue

        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=linewidth,
                                    edgecolor='none',facecolor=facecolor, alpha=0.1)
        ax.add_patch(rect)
        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=linewidth,
                                    edgecolor=edgecolor,facecolor='none',linestyle='-', alpha=alpha)
        ax.add_patch(rect)
        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1], linewidth=0,
                                    edgecolor=edgecolor,facecolor='none',linestyle='-', hatch=hatch, alpha=0.2)
        ax.add_patch(rect)

    plt.xticks([], [])
    plt.yticks([], [])

    legend_elements = [Patch(facecolor=(1, 0, 0.45), edgecolor=(1, 0, 0.45),
                                label='Table', hatch='//////', alpha=0.3),
                        Patch(facecolor=(0.95, 0.6, 0.1), edgecolor=(0.95, 0.6, 0.1),
                                label='Table (rotated)', hatch='//////', alpha=0.3)]
    plt.legend(handles=legend_elements, bbox_to_anchor=(0.5, -0.02), loc='upper center', borderaxespad=0,
                    fontsize=10, ncol=2)
    plt.gcf().set_size_inches(10, 10)
    plt.axis('off')

    if out_path is not None:
      plt.savefig(out_path, bbox_inches='tight', dpi=150)

    return fig

def objects_to_crops(img, tokens, objects, class_thresholds, padding=10):
    """
    Process the bounding boxes produced by the table detection model into
    cropped table images and cropped tokens.
    """

    table_crops = []
    for obj in objects:
        if obj['score'] < class_thresholds[obj['label']]:
            continue

        cropped_table = {}

        bbox = obj['bbox']
        bbox = [bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding]

        cropped_img = img.crop(bbox)

        table_tokens = [token for token in tokens if iob(token['bbox'], bbox) >= 0.5]
        for token in table_tokens:
            token['bbox'] = [token['bbox'][0]-bbox[0],
                             token['bbox'][1]-bbox[1],
                             token['bbox'][2]-bbox[0],
                             token['bbox'][3]-bbox[1]]

        # If table is predicted to be rotated, rotate cropped image and tokens/words:
        if obj['label'] == 'table rotated':
            cropped_img = cropped_img.rotate(270, expand=True)
            for token in table_tokens:
                bbox = token['bbox']
                bbox = [cropped_img.size[0]-bbox[3]-1,
                        bbox[0],
                        cropped_img.size[0]-bbox[1]-1,
                        bbox[2]]
                token['bbox'] = bbox

        cropped_table['image'] = cropped_img
        cropped_table['tokens'] = table_tokens

        table_crops.append(cropped_table)

    return table_crops


def detect_table(path):
    model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-detection", revision="no_timm")
    model.config.id2label
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    print("")
    print(device)
    # let's load an example image
    #file_path = hf_hub_download(repo_id="/content/123.png", repo_type="dataset", filename="image.png")
    image = Image.open(path).convert("RGB")
    # let's display it a bit smaller
    width, height = image.size

    detection_transform = transforms.Compose([
    MaxResize(800),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    pixel_values = detection_transform(image).unsqueeze(0)
    pixel_values = pixel_values.to(device)
    with torch.no_grad():
        outputs = model(pixel_values)
    outputs.logits.shape
    id2label = model.config.id2label
    id2label[len(model.config.id2label)] = "no object"
    objects = outputs_to_objects(outputs, image.size, id2label)
    tokens = []
    detection_class_thresholds = {
        "table": 0.5,
        "table rotated": 0.5,
        "no object": 10
    }
    crop_padding = 10

    tables_crops = objects_to_crops(image, tokens, objects, detection_class_thresholds, padding=0)
    cropped_table = tables_crops[0]['image'].convert("RGB")
    if not os.path.exists(os.path.join(path,"temp")):
        os.makedirs(os.path.join(os.path.dirname(path),"temp"),exist_ok=True)
    cropped_table.save(os.path.join(os.path.dirname(path),"temp","cropped.jpg"),quality=100, subsampling=0)
    print("detected")


def extract_table(path):
    table_engine = PPStructure(show_log=True,structure_version="PP-StructureV2",layout=True
                        #    det_model_dir="Website\\fastapi\\Extract\\PaddleOCR\\ppstructure\\inference\\ch_ppocr_server_v2.0_det_infer",
                        #    rec_model_dir="Website\\fastapi\\Extract\\PaddleOCR\\ppstructure\\inference\\ch_ppocr_server_v2.0_rec_infer",
                        #    table_model_dir="Website\\fastapi\\Extract\\PaddleOCR\\ppstructure\\inference\\ch_ppstructure_mobile_v2.0_SLANet_infer"
    )
    img_path = path
    img = cv2.imread(img_path)
    result = table_engine(img)
    #save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])
    res_file,res_ext = os.path.splitext(Path(path).name)
    html=''
    if not os.path.isfile(f"{os.path.join(os.path.dirname(path),'table')}.html"):
        html=''
    else:
        with open(f"{os.path.join(os.path.dirname(path),'table')}.html",'r',encoding="utf-8") as f:
            html = f.read()
            f.close()
    print("&&&&&&&&&&&&&")
    print(html)
    print("&&&&&&&&&&&&&&&")
    main_soup = BeautifulSoup(html,'html5lib')
    for line in result:
        line.pop('img')
        #res = json.loads(line)
        if line["type"] == "table":
            page_html = line["res"]["html"]
            page1 = BeautifulSoup(page_html,'html5lib')
            ############################## changing thead to tbody
            table = page1.find('table')
            thead = table.find('thead')
            if thead is not None:
                tr = thead.findAll("tr")
                thead.extract
                tbody = table.find('tbody')
                for idx,t in enumerate(tr):
                    tbody.insert(idx,t)
            #######################
            
            table_main = main_soup.find("table")
            if table_main is None:
                body = main_soup.find('body')
                body.append(page1.find('table'))
            ###############################################
            else:
                tbody_main = table_main.find('tbody')
                # print("tbody_main")
                # print(tbody_main)
                header_main = tbody_main.find('tr')
                head_main = header_main.find_all('td')
                table = page1.find('table')
                print("page1")
                tbody = table.find('tbody')
                header = tbody.find('tr')
                print(header)
                head = header.find_all("td")
                print(head)
                if len(head) == len(head_main):
                    print("flag")
                    flag = len(head)
                    for idx,h in enumerate(head_main):
                        # print("main")
                        # print(h.string)
                        # print("no main")
                        head[idx].string
                        if h.string.strip() == head[idx].string:
                            flag -=1
                            print(flag)
                    if flag<len(head):
                        tr = tbody.find_all('tr')
                        for idx,t in enumerate(tr):
                            if idx==0:
                                continue
                            tbody_main.append(t)
                    else:
                        tr = tbody.find_all('tr')
                        for idx,t in enumerate(tr):
                            tbody_main.append(t)
        #######################################
            print(line)
            #print(res)
            print(html)
            with open(f"{os.path.join(os.path.dirname(path),'table')}.html",'w',encoding="utf-8") as f:
                print("htmltbale")
                f.write(main_soup.prettify())
                f.close()
    # if os.path.isfile(img_path):
    #     os.remove(img_path)

######################################## Extraction END ##############################
        
#########################################Extract Call #############################

def extract_call(path):
    with open(os.path.join(path,"status.json"),'r') as f:
        status = json.load(f)
        print(status)
        for s in status:
            if not s["status"]:
                # detect_table(os.path.join(path,s['filename']))
                extract_table(os.path.join(path,s['filename']))
                s['status'] = True
        # json.dump(status,f)
        f.close()
    with open(os.path.join(path,"status.json"),'w') as f:
        print("no data to process")
        json.dump(status,f)
        f.close()
     
# def identify_data_type(data):
#     if data.isalnum():
#         return 'VARCHAR(100)'
#     elif is_float(data):
#         return 'DOUBLE(100,10)'
#     elif data.isnumeric():
#         return 'INT(100)'
#     try:

def convert_to_standard_date_format(date_string):
    try:
        parsed_date = parser.parse(date_string)
        standard_date_format = parsed_date.strftime("%Y-%m-%d")
        return standard_date_format
    except (ValueError, parser.ParserError):
        return None

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

@app.post("/upload_files/{tablename}")
async def index(tablename:str,files:List[UploadFile] = File(...),Authorization:Annotated[str | None,Header()] = None ):
    authorization_token = Authorization.split(" ")[1].encode('ascii')
    try:
        token = jwe.decrypt(authorization_token,settings.AES_SECRET_KEY)
        token = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return {"message":"Invalid Token","redirect":False}
    except Exception as e:
         return {"message":"cant decrypt","redirect":False}
    userid = token['userid']
    # try:
    path = os.path.join("UPLOADED_FILES",userid,tablename)
    os.makedirs(path,exist_ok=True)
    if not os.path.isfile(os.path.join(path,"status.json")):
        print("not exist")
        with open(os.path.join(path,"status.json"),'w')as f:
            em = []
            json.dump(em,f)
            f.close()
    with open(os.path.join(path,"status.json"),'r')as f:
        try:
            status = json.load(f)
        except Exception as e:
            print(e)
            status = []
        f.close()
    for _file in files:
        filename = secure_filename(_file.filename)
        if len(status) == 0:
            with open(os.path.join(path,filename),'wb') as f:
                print("saved")
                shutil.copyfileobj(_file.file,f)
                f.close()
        elif filename in [item["filename"] for item in status]:
            print("continued")
            continue
        else:
            with open(os.path.join(path,filename),'wb') as f:
                print("saved")
                shutil.copyfileobj(_file.file,f)
    pdf2images(path)
    extract_call(path)

    with open(os.path.join(path,"table.html"),'r') as f:
        htmlstring = f.read()

   
    html = BeautifulSoup(htmlstring,"html5lib")
    table  = html.find('table')
    first_row = table.find('tr')
    first_row_data = first_row.find_all('td')   
    type=[]
    column=[]
    for f in first_row_data:
        column.append(f.string)
        if f.string.isalnum():
            type.append('Varchar10')
        elif is_float(f.string):
            type.append('float')
        elif f.string.isdecimal():
            type.append('int')
    
    try:
        mycursor.execute(f"CREATE TABLE `{tablename}` (`Date` DATE  NULL , `Instrument_Id` VARCHAR(100)  NULL , `Amount` INT(100)  NULL , `Type` VARCHAR(100)  NULL , `Balance` INT(100) NULL , `Remarks` VARCHAR(200)  NULL )")
    except:
        pass
    
    
    rows = table.find_all("tr")
    for idx,r in enumerate(rows):
        if idx ==0:
            continue
        data = r.find_all('td')
        print(data)
        data4 = data[4].string.replace(",","").strip()
        data2 = data[2].string.replace(",","").strip()
        data0 = convert_to_standard_date_format(data[0].string.strip())
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("databse store")
        print(data[0].string.strip())
        print(data[1].string.strip())
        print(data2)
        print(data[3].string.strip())
        print(data4)
        print(data[5].string.strip())

        mycursor.execute(f"INSERT INTO `{tablename}`(`Date`, `Instrument_Id`, `Amount`, `Type`, `Balance`, `Remarks`) VALUES ('{data0}','{data[1].string.strip()}','{data2}','{data[3].string.strip()}','{data4}','{data[5].string.strip()}')")
    # except  Exception as e:
    # return {"message":str(e),"redirect":False}
    # # finally:
    # #         _file.file.close()
    mydb.commit()
    return {f"message":"successfull","redirect":True}
            

@app.post("/groups")
async def index(Authorization:Annotated[str | None,Header()] = None ):
    authorization_token = Authorization.split(" ")[1].encode('ascii')
    try:
        token = jwe.decrypt(authorization_token,settings.AES_SECRET_KEY)
        token = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return {"message":"Invalid Token","redirect":False}
    except Exception as e:
         return {"message":"cant decrypt","redirect":False}
    userid = token['userid']

    json_groups={}
    path = os.path.join("UPLOADED_FILES",userid)
    if os.path.exists(path):
        groups = os.listdir(path)
        for g in groups:
            files_list = os.listdir(os.path.join(path,g))
            fil = []
            print(g)
            for f in files_list:
                filename , fileextension = os.path.splitext(f)
                if fileextension.casefold() in ['.jpg','.png','.pdf','.jpeg']:
                    fil.append(filename)
                    print(f)
            json_groups[g] = fil

        print(json_groups)

    return {"result":json_groups,"message":True}

@app.post("/delete/{tablename}")
async def index(tablename:str,Authorization:Annotated[str | None,Header()] = None ):
    authorization_token = Authorization.split(" ")[1].encode('ascii')
    try:
        token = jwe.decrypt(authorization_token,settings.AES_SECRET_KEY)
        token = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return {"message":"Invalid Token","redirect":False}
    except Exception as e:
         return {"message":"cant decrypt","redirect":False}
    userid = token['userid']
    path = os.path.join("UPLOADED_FILES",userid,tablename)
    if os.path.exists(path):
        shutil.rmtree(path)
        mycursor.execute(f"drop table {tablename}")
        mydb.commit()
    return {"message":True}

@app.post("/deleteall")
async def index(Authorization:Annotated[str | None,Header()] = None):
    authorization_token = Authorization.split(" ")[1].encode('ascii')
    try:
        token = jwe.decrypt(authorization_token,settings.AES_SECRET_KEY)
        token = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return {"message":"Invalid Token","redirect":False}
    except Exception as e:
         return {"message":"cant decrypt","redirect":False}
    userid = token['userid']
    path = os.path.join("UPLOADED_FILES",userid)
    if os.path.exists(path):
        all_grps = os.listdir(path)
        for a in all_grps:
            del_path = os.path.join(path,a)
            shutil.rmtree(del_path)
            mycursor.execute(f"drop table {a}")
            mydb.commit()

    return {"message":True}