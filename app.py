import os
import re
from os import path
import sys
import PyPDF2
import glob
import pandas as pd

def ensure_directory_exists(directory_path='pdfs'):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")


def get_pdf_files(directory):
    ensure_directory_exists(directory)
    pdf_files = glob.glob(f"{directory}/*.pdf")  # Search for all PDF files in the directory
    return pdf_files

def read_pdf(pdf_fullpath):
    transaction_data=[]
    try:
        filename = os.path.basename(pdf_fullpath)
        print(f"Reading '{filename}...'")
        readers = PyPDF2.PdfReader(pdf_fullpath)
        pdf_text = ''

        page = 1

        for reader in readers.pages:        
            print(f"---Reading page {page}...")
            pdf_text += (reader.extract_text())
            page +=1    
            data_per_lines = pdf_text.strip().upper().splitlines()
            re_account_date = 'TANGGAL REKENING \:\d+\s\w+\s\d+'
            re_due_date = 'TANGGAL JATUH TEMPO \:\d+\s\w+\s\d+'
            re_account_number = 'NOMOR CUSTOMER\s\:\d+'
            re_credit_quality = 'KUALITAS KREDIT :\w+'
            re_new_bill = 'TAGIHAN BARU :\w+\s\d+.*'
            re_min_bill = 'PEMBAYARAN MINIMUM :\w+\s\d+.*'
            account_number = str(re.findall(re_account_number,pdf_text)[0]).replace('NOMOR CUSTOMER :','').strip()
            account_date = str(re.findall(re_account_date,pdf_text)[0]).replace('TANGGAL REKENING :','').strip()
            due_date = str(re.findall(re_due_date,pdf_text)[0]).replace('TANGGAL JATUH TEMPO :','').strip()
            new_bill = int(''.join(re.findall(r'\d+',str(re.findall(re_new_bill,pdf_text)[0]).replace('TAGIHAN BARU :','').strip())))
            min_bill = int(''.join(re.findall(r'\d+',str(re.findall(re_min_bill,pdf_text)[0]).replace('PEMBAYARAN MINIMUM :','').strip())))*1
            credit_quality = str(re.findall(re_credit_quality,pdf_text)[0]).replace('KUALITAS KREDIT :','').strip()
        # print(pdf_text)
            for line in data_per_lines:
                regex_transaction = '^\d+\-\w+\s\d+\-\w+.*\d$'
                matches = re.findall(regex_transaction,line)
                if matches:
                    re_date = '\d+\-\w+'
                    re_trans_date = str(re.findall(re_date,line)[0]).strip()
                    re_book_date = str(re.findall(re_date,line)[1]).strip()
                    new_line = line.replace(re_trans_date,'').replace(re_book_date,'')
                    last_word = new_line.split()[-1]
                    transaction = str(new_line.replace(last_word,''))
                    transaction = " ".join(transaction.split())
                    transaction_amount = last_word.replace('.','')*1
                    transaction_data.append([account_number,account_date,due_date,credit_quality,re_trans_date,re_book_date,transaction,transaction_amount,new_bill,min_bill,filename])                
            
        df = pd.DataFrame(transaction_data,columns=['NOMOR CUSTOMER','TANGGAL REKENING','TANGGAL JATUH TEMPO','KUALITAS KREDIT','TANGGAL TRANSAKSI','TANGGAL PEMBUKUAN','KETERANGAN','JUMLAH','TAGIHAN BARU','PEMBAYARAN MINIMUM','FILENAME'])
        return df

    except:
        print(f"Failed to read pdf in '{filename}'  Perhaps PDF not exist or it has different format. ")
        return None

def export_to_pdf(transaction_data):
    df = pd.DataFrame(transaction_data,columns=['NOMOR CUSTOMER','TANGGAL REKENING','TANGGAL JATUH TEMPO','KUALITAS KREDIT','TANGGAL TRANSAKSI','TANGGAL PEMBUKUAN','KETERANGAN','JUMLAH','TAGIHAN BARU','PEMBAYARAN MINIMUM','FILENAME'])
    df.to_excel('compiled_bca_estatement_by_tikidata_analytics.xlsx',index=False)
    print('Excel exported!')

def extract_pdf():
    transaction_data = []
    output = pd.DataFrame()
    pdf_folder = os.path.join(os.getcwd(),'pdfs')
    pdf_files = get_pdf_files(pdf_folder)
    if len(pdf_files)>0:
        print(f" {len(pdf_files)} Pdf files found.")
        for pdf_file in pdf_files:
            data_pdf = read_pdf(pdf_file)
            transaction_data.append(data_pdf)
        output = pd.concat(transaction_data)
        export_to_pdf(output)
    else:
        print(f"Pdf not found in {pdf_folder}. Copy BCA Credit Card E-Statement to '{pdf_folder}' first.")
    # if count_pdf_files == 0:
    #     print(f"PDF E-Statement dari KlikBCA disimpen di folder '{pdf_folder}' dulu bang")
    #     sys.exit()
        
extract_pdf() 