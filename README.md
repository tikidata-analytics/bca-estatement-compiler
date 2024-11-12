# BCA E-Statement Compiler

Do you find it's difficult in compiling your BCA Credit Card E-Statement?
Yes. Me too! Sometimes i had to compile like a year cycle to know how much debt do i have and stuff
That's why i decided to build this tool to help us extracting informations from BCA Credit Card E-Statement PDF files.

This tool would help you to compile your PDF files at once and will export the data to Excel so you can use them later.
The extracted columns are:
* NOMOR CUSTOMER
* TANGGAL REKENING
* TANGGAL JATUH TEMPO
* KUALITAS KREDIT
* TANGGAL TRANSAKSI
* TANGGAL PEMBUKUAN
* KETERANGAN
* JUMLAH TAGIHAN
* TAGIHAN BARU
* PEMBAYARAN MINIMUM
* FILENAME

The tool isn't perfect yet. There are some row won't extracted such as:
* Any row with "CR" at the end of their lines
* Multiple Rows (such as forex / transaction in foreign currency) won't extracted
If you could some help to improve this tool, let's collab!



