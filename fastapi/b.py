from bs4 import BeautifulSoup 


with open("E:\\PreciseExtract\\Website\\fastapi\\UPLOADED_FILES\\80908932720233265373125914068709548619\\results\\80.html",'r') as f:
    content = f.read()

html='''
<html>
 <head>
 </head>
 <body>
  <table>
   <thead>
    <tr>
     <td>
      Date
     </td>
     <td>
      Instrument ID
     </td>
     <td>
      Amount
     </td>
     <td>
      Type
     </td>
     <td>
      Balance
     </td>
     <td>
      Remarks
     </td>
    </tr>
   </thead>
   <tbody>
    <tr>
     <td>
      15/12/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      DR
     </td>
     <td>
      2,094.01
     </td>
     <td>
      05216015000619
     </td>
    </tr>
    <tr>
     <td>
      12/12/2022
     </td>
     <td>
     </td>
     <td>
      9100.00
     </td>
     <td>
      CR
     </td>
     <td>
      10,194.01
     </td>
     <td>
      UPI/234678412099/P2V/nay.kothari123- 1@okhdfcbank/N
     </td>
    </tr>
    <tr>
     <td>
      12/12/2022
     </td>
     <td>
     </td>
     <td>
      500.00
     </td>
     <td>
      DR
     </td>
     <td>
      1,094.01
     </td>
     <td>
      ATMWDR234613017371BDBG BLOCKBKC BANDRA
     </td>
    </tr>
    <tr>
     <td>
      11/12/2022
     </td>
     <td>
     </td>
     <td>
      5000.00
     </td>
     <td>
      CR
     </td>
     <td>
      6,094.01
     </td>
     <td>
      UPI/234543148645/P2V/shahshailsh0707@okhdfc bank/S
     </td>
    </tr>
    <tr>
     <td>
      03/12/2022
     </td>
     <td>
     </td>
     <td>
      16.00
     </td>
     <td>
      CR
     </td>
     <td>
      1,094.01
     </td>
     <td>
      05212011023472:IntPd:01-09-2022 to 30-11-2022
     </td>
    </tr>
    <tr>
     <td>
      16/1/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      DR
     </td>
     <td>
      1,078.01
     </td>
     <td>
      05216015000619
     </td>
    </tr>
    <tr>
     <td>
      15/11/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      CR
     </td>
     <td>
      9,178.01
     </td>
     <td>
      UPI/231916286245/P2V/nay.kothari123- 1@okhdfebank/N
     </td>
    </tr>
    <tr>
     <td>
      15/10/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      DR
     </td>
     <td>
      1,078.01
     </td>
     <td>
      05216015000619
     </td>
    </tr>
    <tr>
     <td>
      13/10/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      CR
     </td>
     <td>
      9,178.01
     </td>
     <td>
      NEFT_IN:KKBKH22286926474/0045/NAYNESH CHANDRAKANTKOTHARI
     </td>
    </tr>
    <tr>
     <td>
      15/09/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      DR
     </td>
     <td>
      1,078.01
     </td>
     <td>
      05216015000619
     </td>
    </tr>
    <tr>
     <td>
      04/09/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      CR
     </td>
     <td>
      9,178.01
     </td>
     <td>
      NEFT_IN:KKBKH22247867272/0040/NAYNESH CHANDRAKANTKOTHARI
     </td>
    </tr>
    <tr>
     <td>
      04/09/2022
     </td>
     <td>
     </td>
     <td>
      22.00
     </td>
     <td>
      CR
     </td>
     <td>
      1,078.01
     </td>
     <td>
      05212011023472:Int.Pd:01-06-2022 to 31-08-2022
     </td>
    </tr>
    <tr>
     <td>
      15/08/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      DR
     </td>
     <td>
      1,056.01
     </td>
     <td>
      05216015000619
     </td>
    </tr>
    <tr>
     <td>
      04/08/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      CR
     </td>
     <td>
      9,156.01
     </td>
     <td>
      NEFT_IN:KKBKH22216911633/0045/NAYNESH CHANDRAKANTKOTHARI
     </td>
    </tr>
    <tr>
     <td>
      15/07/2022
     </td>
     <td>
     </td>
     <td>
      8100.00
     </td>
     <td>
      DR
     </td>
     <td>
      1,056.01
     </td>
     <td>
      05216015000619
     </td>
    </tr>
   </tbody>
  </table>
 </body>
</html>
'''
main_soup = BeautifulSoup(html,'html5lib')
page1 = BeautifulSoup(content,'html5lib')
###################
table = page1.find('table')
thead = table.find('thead')
if thead is not None:
    tr = thead.findAll("tr")
    thead.extract
    tbody = table.find('tbody')
    for idx,t in enumerate(tr):
        tbody.insert(idx,t)

# print(page1.prettify())
##############

table = main_soup.find('table')
thead = table.find('thead')
if thead is not None:
    tr = thead.findAll("tr")
    thead.extract
    tbody = table.find('tbody')
    for idx,t in enumerate(tr):
        tbody.insert(idx,t)

# print(main_soup.prettify())


table_main = main_soup.find("table")
if table_main is None:
    body = main_soup.find('body')
    body.append(page1.find('table'))
else:
    tbody_main = table_main.find('tbody')
    header_main = tbody_main.find('tr')
    head_main = header_main.findAll('td')
    table = page1.find('table')
    tbody = table.find('tbody')
    header = tbody.find('tr')
    head = header.findAll("td")

    if len(head) == len(head_main):
        print("flag")
        flag = len(head)
        for idx,h in enumerate(head_main):
            # print("main")
            # print(h.string)
            # print("no main")
            # print(head[idx].string)
            if h.string.strip() == head[idx].string.strip():
                flag -=1
                print(flag)
            
        if flag==0:
            tr = tbody.find_all('tr')
            for idx,t in enumerate(tr):
                if idx==0:
                    continue
                tbody_main.append(tr)
        else:
            tr = tbody.find_all('tr')
            for idx,t in enumerate(tr):
                tbody_main.append(tr)

            

        

# print(page1.prettify())


# if len(html)==0:
#     body = main_soup.find('body')
#     body.append(soup.find('table'))

#     print(main_soup.prettify())
# else:
#     ## write to html
#     print("wrote to html")




# print(table.prettify())

# print(soup.prettify)