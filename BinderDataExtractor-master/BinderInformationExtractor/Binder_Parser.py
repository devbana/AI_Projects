import io
import multiprocessing as mp
import os
import pprint
import docx2txt
import nltk
import spacy
import win32com.client
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
from spacy.matcher import Matcher
import pythoncom
import BinderInformationExtractor.Utilities as Utilities


class BinderParser(object):
    inputString = ''
    tokens = []
    lines = ""
    sentences = []
    company = []
    policyperiod = []
    insuredaddress = ""

    def __init__(self, Binder):
        # nlp = spacy.load('en_core_web_sm')
        nlp = spacy.load('en')
        self.__matcher = Matcher(nlp.vocab)
        self.__Binder = Binder
        self.__details = {
            'Insured Name': None,
            'Insured Address': None,
            'Insured State':None,
            'Policy Number': None,
            'Broker Name': None,
            'Broker Company': None,
            'Broker Address': None,
            'Broker State': None,
            'Policy Effective Date': None,
            'Policy Expiration Date': None,
            'Commission': None,
            'Company': None,
            'Currency': None,
            'Premium': None,
            'Policy Form': None,
            'Waiting Period': None,
            'Underwriter Name': None,
            'Underwriter Contact': None,
            'Underwriter EmailID': None,
            'No of pages': None
        }
        if not isinstance(self.__Binder, io.BytesIO):
            ext = os.path.splitext(self.__Binder)[1].split('.')[1]
        else:
            ext = self.__Binder.name.split('.')[1]
        self.__text_raw = extract_text(self.__Binder, '.' + ext)[0]
        if ext in ('pdf', 'PDF'):
            self.__text_with_laparams = extract_text(self.__Binder, '.' + ext)[1]
        else:
            self.__text_with_laparams = self.__text_raw
        # self.tokenize(self.__text_raw)
        self.__text = ' '.join(self.__text_raw)
        self.__nlp = nlp(self.__text_raw)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_binders_details()

    def get_extracted_data(self):
        return self.__details
        # return self.__text_raw

    def __get_binders_details(self):

        commission = Utilities.extract_commission(self.__text_raw)
        premium = Utilities.extract_premium(self.__text_raw)
        company = Utilities.extract_insurance_company(self.__nlp)
        policyperiod = Utilities.extract_policy_period(self.__text_raw)
        if len(policyperiod) == 0:
            policyperiod = Utilities.extract_policy_period(self.__text_with_laparams)
        brokercompany = Utilities.extract_brokercompany(self.__text_raw)
        brokeraddress = Utilities.extract_brokeraddress(self.__text_with_laparams)
        insuredaddress = Utilities.extract_insuredaddress(self.__text_raw, brokeraddress)
        policynumber = Utilities.extract_policy_number(self.__text_with_laparams)

        underwriter_name = Utilities.extract_underwriter_name(self.__text_raw, self.__matcher)
        underwriter_email = Utilities.extract_underwriter_Email(self.__text_raw)
        underwriter_contact = Utilities.extract_underwriter_contact(self.__text_raw)
        broker_name = Utilities.extract_broker_name(self.__text_with_laparams, self.__matcher)
        waiting_period = Utilities.extract_waiting_time(self.__text_with_laparams)
        policy_form = None#Utilities.extract_policy_form(self.__text_raw)
        no_of_pages = get_number_of_pages(self.__Binder)
        extract_broker_state = Utilities.extract_broker_state(str(brokeraddress))
        if insuredaddress is not None:
            extract_insured_state = Utilities.extract_insured_state(str(insuredaddress[0]))
        else:
            extract_insured_state =None



        self.__details['Commission'] = commission
        self.__details['Premium'] = premium
        if company.size == 1:
            self.__details['Company'] = company[0]
        else:
            self.__details['Company'] = company[0:]
        self.__details['Currency'] = Utilities.extract_currency(self.__nlp, self.__text_raw)
        if len(policyperiod) != 0:
            self.__details['Policy Effective Date'] = policyperiod[0]
        else:
            self.__details['Policy Effective Date'] = None
        if len(policyperiod) != 0:
            self.__details['Policy Expiration Date'] = policyperiod[1]
        else:
            self.__details['Policy Expiration Date'] = None
        if brokercompany is not None and len(brokercompany) == 1:
            self.__details['Broker Company'] = brokercompany[0]
        elif brokercompany is not None:
            self.__details['Broker Company'] = brokercompany
        if brokeraddress is not None and len(brokeraddress) == 1:
            self.__details['Broker Address'] = brokeraddress[0]
        elif brokeraddress is not None:
            self.__details['Broker Address'] = brokeraddress
        if insuredaddress is not None:
            self.__details['Insured Address'] = insuredaddress[0]
            self.__details['Insured Name'] = insuredaddress[1].replace(' s', '')
        else:
            insuredaddress = Utilities.extract_insuredaddress(self.__text_with_laparams, brokeraddress)
            if insuredaddress is not None:
                self.__details['Insured Address'] = insuredaddress[0]
                self.__details['Insured Name'] = insuredaddress[1].replace(' s', '')

        if policynumber is not None:
            for dd in policynumber:
                if len(dd) > 7:
                    self.__details['Policy Number'] = dd
                    break
        if underwriter_email is not None:
            self.__details['Underwriter EmailID'] = underwriter_email

        if underwriter_contact is not None:
            self.__details['Underwriter Contact'] = underwriter_contact

        if underwriter_name is not None:
            self.__details['Underwriter Name'] = underwriter_name.replace('\'','')

        if broker_name is not None:
            self.__details['Broker Name'] = broker_name.replace('\'','')

        if waiting_period is not None:
            self.__details['Waiting Period'] = waiting_period

        if policy_form is not None:
            self.__details['Policy Form'] =policy_form

        if no_of_pages is not None:
            self.__details['No of pages'] = no_of_pages

        if extract_broker_state is not None:
            self.__details['Broker State'] = extract_broker_state

        if extract_insured_state is not None:
            self.__details['Insured State'] = extract_insured_state

        return


def binder_result_wrapper(BinderData):
    parser = BinderParser(BinderData)
    return parser.get_extracted_data()


def extract_text(file_path, extension):
    '''
    Wrapper function to detect the file extension and call text extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    text_withlaparams = ''
    if extension == '.pdf':
        for page in extract_text_from_pdf(file_path):
            text += ' ' + page
        text_withlaparams = extract_text_from_pdf_with_laparams(file_path)
    elif extension == '.docx':
        text = extract_text_from_docx(file_path)
    elif extension == '.doc':
        text = extract_text_from_doc(file_path)
    return text, text_withlaparams


def extract_text_from_pdf(pdf_path):
    '''
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted (remote or local)
    :return: iterator of string of extracted text
    '''
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    if not isinstance(pdf_path, io.BytesIO):
        # extract text from local pdf file
        with open(pdf_path, 'rb') as fh:
            try:
                for page in PDFPage.get_pages(fh,
                                              caching=True,
                                              check_extractable=True):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(resource_manager, fake_file_handle)
                    page_interpreter = PDFPageInterpreter(resource_manager, converter)
                    page_interpreter.process_page(page)
                    text = fake_file_handle.getvalue()
                    yield text

                    # close open handles
                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                return
    else:
        # extract text from remote pdf file
        try:
            for page in PDFPage.get_pages(pdf_path,
                                          caching=True,
                                          check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
                page_interpreter = PDFPageInterpreter(resource_manager, converter)
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield text

                # close open handles
                converter.close()
                fake_file_handle.close()
        except PDFSyntaxError:
            return


def extract_text_from_pdf_with_laparams(pdf_path):
    text = ""
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(pdf_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    caching = True
    pagenos = set()

    for PageNumer, page in enumerate(
            PDFPage.get_pages(fp, pagenos, password=password, caching=caching, check_extractable=True)):
        interpreter.process_page(page)
        text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def extract_text_from_docx(doc_path):
    '''
    Helper function to extract plain text from .docx files

    :param doc_path: path to .docx file to be extracted
    :return: string of extracted text
    '''
    try:
        temp = docx2txt.process(doc_path)
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
    except KeyError:
        return ' '


def extract_text_from_doc(doc_path):
    '''
    Helper function to extract plain text from .doc files

    :param doc_path: path to .doc file to be extracted
    :return: string of extracted text
    '''
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    wb = word.Documents.Open(doc_path)
    doc = word.ActiveDocument
    return doc.Range().Text


def get_number_of_pages(file_name):
    try:
        if file_name.endswith('.pdf') or file_name.endswith('.PDF') or file_name.endswith('.Pdf'):
            if isinstance(file_name, io.BytesIO):
            # for remote pdf file
                count = 0
                for page in PDFPage.get_pages(file_name,
                                          caching=True,
                                          check_extractable=True):
                    count += 1
                return count
            else:
                # for local pdf file
                if file_name.endswith('.pdf'):
                    count = 0
                    with open(file_name, 'rb') as fh:
                        for page in PDFPage.get_pages(fh,
                                                  caching=True,
                                                  check_extractable=True):
                            count += 1
                    return count
        elif file_name.endswith('.doc'):
            from win32com.client import Dispatch
            word = Dispatch('Word.Application')
            word.Visible = False
            word = word.Documents.Open(file_name)
            # get number of sheets
            word.Repaginate()
            return word.ComputeStatistics(2)

        else:
            return None
    except PDFSyntaxError:
        return None



if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())

    Binder = []

    for root, directories, filenames in os.walk('Binder'):
        for filename in filenames:
            file = os.path.join(root, filename)
            Binder.append(file)
    results = [pool.apply_async(binder_result_wrapper, args=(x,)) for x in Binder]
    results = [p.get() for p in results]
    pprint.pprint(results)
