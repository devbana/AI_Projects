import traceback
import re
import docx2txt
import nltk
import spacy
import numpy as np
import pyap
import phonenumbers
import BinderInformationExtractor.constants as cs
import usaddress

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
    try:
        try:
            import textract
        except ImportError:
            return ' '
        temp = textract.process(doc_path).decode('utf-8')
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
    except KeyError:
        return ' '


def extract_currency(nlp_text, inputstring):
    en_money = {}
    cons_money = {'$', '€', '£', '¥', "USD"}
    final_currency = {}
    for en in nlp_text.ents:
        if en.label_ in 'MONEY':
            en_money[en.text] = en.text
    for curr in en_money:
        for sym in cons_money:
            if (sym in curr):
                final_currency = sym
                return final_currency

    sentences = nltk.sent_tokenize(inputstring)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
        sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
        if re.search('premium', sen):
            # for sentence in sentences:
            sen1 = " ".join([words[0] for words in sentence])
            for sym in cons_money:
                if (sym in sen1):
                    final_currency = sym
                    return final_currency


def extract_commission(inputstring):
    commission = []
    pattr = '[\d]+[.]*[\d]{0,2}[\s]*[%](?= |$)'
    # chunked = []
    # grammer = "NP: {<CD><NN>}"
    try:
        # sentences = ''
        # lines = [el.strip() for el in inputstring if len(el) > 0]  # Splitting on the basis of newlines
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            if re.search('commission', sen):
                startpos = re.search('commission', sen)
                nlp = spacy.load('en')
                doc = nlp(sen[startpos.end():len(sen)])
                for en in doc.ents:
                    if en.label_ is 'PERCENT':
                        commission = en.text
                        return re.findall(pattr, commission)


    except Exception as e:
        print(traceback.format_exc())
        print(e)
    if commission:
        commission = re.sub('[^0-9.%]', '', commission)
        return commission
    else:
        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            if re.search('commission', sen):
                starpos = re.search('commission', sen)
                ad = re.findall(pattr, sen[starpos.end():len(sen)])
                if ad:
                    return ad

        # nlp = spacy.load('en')
        # doc = nlp(inputstring)
        # for en in doc.ents:
        #   if en.label_ is 'PERCENT':
        #       commission = en.text
        #      break
    if commission:
        commission = re.sub('[^0-9.%]', '', commission)
        return commission


def extract_premium(inputstring):
    premium = []
    dummyprem = []
    cons_money = {'$', '€', '£', '¥', "USD"}
    try:
        # sentences = ''
        # lines = [el.strip() for el in inputstring if len(el) > 0]  # Splitting on the basis of newlines
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        ################ search policy premuim #################

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            if re.search('policy premium', sen):
                sen1 = " ".join([words[0] for words in sentence])
                startpre = re.search('policy premium', sen1.lower())
                strlen = len(sen1)
                if strlen > (startpre.start() + 100):
                    doc = sen1[startpre.start():startpre.start() + 50]
                else:
                    doc = sen1[startpre.start():len(sen1)]
                nlp = spacy.load('en')
                doc = nlp(doc)
                for en in doc.ents:
                    if en.label_ is 'MONEY':
                        premium = en.text
                        premium = re.sub('[^0-9,.%]', '', premium)
                        return premium

        ################ search total premium ################

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            if re.search('total premium', sen):
                sen1 = " ".join([words[0] for words in sentence])
                startpre = re.search('total premium', sen1.lower())
                strlen = len(sen1)
                if strlen > (startpre.start() + 100):
                    doc = sen1[startpre.start():startpre.start() + 50]
                else:
                    doc = sen1[startpre.start():len(sen1)]
                nlp = spacy.load('en')
                doc = nlp(doc)
                for en in doc.ents:
                    if en.label_ is 'MONEY':
                        premium = en.text
                        premium = re.sub('[^0-9,.%]', '', premium)
                        return premium
        ################ searching policy ################

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            if re.search('premium', sen):
                sen1 = " ".join([words[0] for words in sentence])
                startpre = re.search('premium', sen1.lower())
                strlen = len(sen1)
                if strlen > (startpre.start() + 100):
                    doc = sen1[startpre.start():startpre.start() + 50]
                else:
                    doc = sen1[startpre.start():len(sen1)]
                nlp = spacy.load('en')
                doc = nlp(doc)
                for en in doc.ents:
                    if en.label_ is 'MONEY':
                        premium = en.text
                        premium = re.sub('[^0-9,.%]', '', premium)
                        return premium

        ########################### searching by Regex policy premium =====================================================

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            if re.search('policy premium', sen):
                sen1 = " ".join([words[0] for words in sentence])
                pos = re.search('policy premium', sen1.lower())
                dummyprem = re.findall('[USD£$€]+[\s]*\d+[,]*\d+[.]*\d+', sen[pos.start():len(sen1)])
                for prem in dummyprem:
                    for curr in cons_money:
                        if curr in prem:
                            premium = prem
                            return premium
        ########################### searching by Regex total premium =====================================================

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            if re.search('total premium', sen):
                sen1 = " ".join([words[0] for words in sentence])
                pos = re.search('total premium', sen1.lower())
                dummyprem = re.findall('[USD£$€]+[\s]*\d+[,]*\d+[.]*\d+', sen1[pos.start():len(sen1)])
                for prem in dummyprem:
                    for curr in cons_money:
                        if curr in prem:
                            premium = prem
                            return premium
        ########################### searching by Regex premium =====================================================

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            if re.search('premium', sen):
                sen1 = " ".join([words[0] for words in sentence])
                pos = re.search('premium', sen1.lower())
                dummyprem = re.findall('[USD£$€]+[\s]*\d+[,]*\d+[.]*\d+', sen1[pos.start():len(sen1)])
                for prem in dummyprem:
                    for curr in cons_money:
                        if curr in prem:
                            premium = prem
                            return premium

    except Exception as e:
        print(traceback.format_exc())
        print(e)

    return premium


def extract_insurance_company(nlp_text):
    cons_insurance = ["AIG",
                      ]
    insurance_org = []
    finalinsurance = []

    for en in nlp_text.ents:
        if en.label_ is 'ORG':
            insurance_org.append(en.text)

    for dd1 in cons_insurance:
        for dd2 in insurance_org:
            if dd1 in dd2:
                finalinsurance.append(dd1)

    insurancenames = np.array(finalinsurance)
    return np.unique(insurancenames)


def extract_policy_period(inputstring):
    policyperiod = []
    sentences = nltk.sent_tokenize(inputstring)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    try:
        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('policy period', sen.lower()):
                result = re.search('policy period', sen.lower())
                a1 = re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", sen[result.start():len(sen)])
                if len(a1) != 0:
                    policyperiod = a1
                    return policyperiod
                elif len(re.findall(r"[\d]{1,2}-[a-zA-Z]{2,4}-[\d]{4}", sen[result.start():len(sen)])) != 0:
                    a2 = re.findall(r"[\d]{1,2}-[a-zA-Z]{2,4}-[\d]{4}", sen[result.start():len(sen)])
                    policyperiod = a2
                    return policyperiod
                elif len(re.findall(r"[a-zA-Z]+\s*[\d]{1,2}\s*,\s*[\d]{4}", sen[result.start():len(sen)])) != 0:
                    a3 = re.findall(r"[a-zA-Z]+\s*[\d]{1,2}\s*,\s*[\d]{4}", sen[result.start():len(sen)])
                    if len(a3) != 0:
                        policyperiod = a3
                        return policyperiod
        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('period', sen.lower()):
                result = re.search('period', sen.lower())
                a1 = re.findall(r"[0-9a-zA-Z]+[\s]+[a-zA-Z]*[\s]+[\d]{1,4}(?= |$)", sen[result.start():len(sen)])
                if len(a1) != 0:
                    policyperiod = a1
                    return policyperiod

    except Exception as e:
        print(traceback.format_exc())
        print(e)

    return policyperiod


def extract_brokercompany(inputstring):
    brokerdict = {
        'Marsh': 'Marsh USA, Inc'
    }
    finalbrokercompany = []
    try:
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in sentence])  # string of words in sentence
            for brokercomp in brokerdict.keys():
                if re.search(brokercomp.lower(), sen):
                    finalbrokercompany = brokerdict[brokercomp]
                    break

    except Exception as e:
        print(traceback.format_exc())
        print(e)

    return finalbrokercompany


def extract_insuredaddress(inputstring, brokeraddress):
    global b, addrs, sentences2
    addresses = []
    ab = {}
    ac = {}
    sentences1 = ""
    istartpos = 0
    finaladdress = ""
    insuredaddress = ""
    cnt = 0
    ad = {}
    sen = ""
    a = 0
    alladdress = ""
    insuredname = ""
    pattr = '(?:^|(?<= ))[\d]{4} [\w]+.*,[\s]+[A-Z]{2} \d{5}[-]*[\d]*'
    pattr1 = '(?:^|(?<= ))[\d]{4}[\s]+[\w]+[\s]+[\d]{0,3}[\s]+[A-Za-z\s]*[\d]{5}\s+United States of America(?= |$)'
    try:
        insuredsentences = nltk.sent_tokenize(inputstring)
        insuredsentences = [nltk.word_tokenize(sent) for sent in insuredsentences]  # Tokenize the individual lines
        insuredsentences = [nltk.pos_tag(sent) for sent in insuredsentences]

        for insentence in insuredsentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in insentence])  # string of words in sentence
            if re.search('insured', sen):
                sentences1 = " ".join([words[0] for words in insentence])
                istartpos = re.search('insured', sentences1.lower())
                # insuredcount = re.findall('insured', sentences1.lower())
                # cnt = re.findall('insured', sentences1.lower())
                ''''if len(sentences1) > (istartpos.end() + 100) & len(insuredcount) == 1:
                    addresses = pyap.parse(sentences1[istartpos.end():istartpos.end() + 100], country='US')
                    if len(brokeraddress)== 1:
                        for addr in addresses:
                            if addr==brokeraddress:
                                continue'''
                # else:
                addresses = pyap.parse(sentences1[istartpos.start():len(sentences1)], country='US')
                if len(addresses) != 0:
                    if len(brokeraddress) != 0:
                        for addr in addresses:
                            addrs = addr.full_address
                            if brokeraddress == addrs:
                                break
                        if brokeraddress == addrs:
                            continue
                    if len(addresses) != 0:
                        break

        if len(addresses) == 1:  # Single Address found
            bb = re.search(addresses[0].full_address, sentences1)
            ab.update({bb.start(): bb.end()})
            cnt = re.findall('insured', sentences1.lower())
            if len(cnt) == 1:
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', sentences1[istartpos.end():bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.,]', '', insuredname)
                return addresses[0].full_address, insuredname.strip()
            else:
                for mm in re.finditer('insured', sen):
                    ad.update({mm.start(0): mm.end(0)})
                for j in sorted(ad):
                    if j < bb.start():
                        a = j
                        continue
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', sentences1[ad[a]:bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                if len(insuredname) > 15:
                    insuredname = insuredname
                    return addresses[0].full_address, insuredname.strip()
                else:
                    for jj in sorted(ad):
                        if jj < a:
                            b = jj
                            continue
                    insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                    insuredname = insuredname.sub('', sentences1[ad[b]:bb.start()])
                    insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                return addresses, insuredname.replace('Insured', '').strip()

        elif len(addresses) > 1:  # Multiple addresses found
            for aa in addresses:
                if re.search(aa.full_address, sentences1):
                    bb = re.search(aa.full_address, sentences1)
                    ab.update({bb.start(): bb.end()})

            for i in sorted(ab):
                if i > istartpos.start():  # address found after Insured Keyword
                    finaladdress = sentences1[i:ab[i]]
                    cnt = re.findall('insured', sentences1.lower())
                    if len(cnt) == 1:
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences1[istartpos.end():i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        return finaladdress, insuredname.strip()
                    else:
                        for mm in re.finditer('insured', sen):
                            ad.update({mm.start(0): mm.end(0)})
                        for j in sorted(ad):
                            if j < i:
                                a = j
                                continue
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences1[ad[a]:i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        if len(insuredname) < 15:
                            insuredname = insuredname
                            return finaladdress, insuredname.strip()
                        else:
                            for jj in sorted(ad):
                                if jj < a:
                                    b = jj
                                    continue
                        return finaladdress, insuredname.strip()

        ######################### Search For Insured Name in String by using Regex1 ################################

        for insentence in insuredsentences:  # Using Regular Expression
            sen = " ".join([words[0].lower() for words in insentence])  # string of words in sentence
            if re.search('insured', sen):
                sentences1 = " ".join([words[0] for words in insentence])
                istartpos = re.search('insured', sentences1.lower())
                # cnt = re.findall('insured', sentences1.lower())
                addresses = re.findall(pattr, sentences1)
                if len(addresses) != 0:
                    break

        if len(addresses) == 1:
            bb = re.search(addresses[0], sentences1)
            ab.update({bb.start(): bb.end()})
            cnt = re.findall('insured', sentences1.lower())
            if len(cnt) == 1:
                istartpos = re.search('insured', sentences1.lower())
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', sentences1[istartpos.end():bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.,]', '', insuredname)
                return addresses[0], insuredname.strip()
            else:
                for mm in re.finditer('insured', sen):
                    ad.update({mm.start(0): mm.end(0)})
                for j in sorted(ad):
                    if j < bb.start():
                        a = j
                        continue
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', sentences1[ad[a]:bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                if len(insuredname) > 15:
                    insuredname = insuredname
                    return addresses[0].full_address, insuredname.strip()
                else:
                    for jj in sorted(ad):
                        if jj < a:
                            b = jj
                            continue
                    insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                    insuredname = insuredname.sub('', sentences1[ad[b]:bb.start()])
                    insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                return addresses, insuredname.replace('Insured', '').strip()

        elif len(addresses) > 1:  # Multiple addresses found
            for aa in addresses:
                if re.search(aa.full_address, sentences1):
                    bb = re.search(aa.full_address, sentences1)
                    ab.update({bb.start(): bb.end()})

            for i in sorted(ab):
                if i > istartpos.start():  # address found after Insured Keyword
                    finaladdress = sentences1[i:ab[i]]
                    cnt = re.findall('insured', sentences1.lower())
                    if len(cnt) == 1:
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences1[istartpos.end():i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                    else:
                        for mm in re.finditer('insured', sen):
                            ad.update({mm.start(0): mm.end(0)})
                        for j in sorted(ad):
                            if j < i:
                                a = j
                                continue
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences1[ad[a]:i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        if len(insuredname) < 15:
                            insuredname = insuredname
                            return finaladdress, insuredname
                        else:
                            for jj in sorted(ad):
                                if jj < a:
                                    b = jj
                                    continue
                        return finaladdress, insuredname.strip()

        ######################### Search For Insured Name in String by using Regex2 ################################
        sentences2 = ""
        for insentence in insuredsentences:  # Using Regular Expression
            sentences1 = " ".join([words[0] for words in insentence])  # string of words in sentence
            if re.search('insured', sentences1.lower()):
                sentences2 = " ".join([words[0] for words in insentence])
                continue
            if re.search('insured', sentences2.lower()):
                sentences2 += " ".join([words[0] for words in insentence])
                istartpos = re.search('insured', sentences2.lower())
            else:
                sentences2 = ""
            addresses = re.findall(pattr1, sentences2)
            if len(addresses) != 0:
                break
            else:
                sentences2 = ""

        if len(addresses) == 1:
            bb = re.search(addresses[0], sentences2)
            ab.update({bb.start(): bb.end()})
            cnt = re.findall('insured', sentences2.lower())
            if len(cnt) == 1:
                istartpos = re.search('insured', sentences2.lower())
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', sentences2[istartpos.end():bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.,]', '', insuredname)
                return addresses[0], insuredname.strip()
            elif len(cnt) == 0:
                return addresses[0], insuredname.strip()
            else:
                for mm in re.finditer('insured', sen):
                    ad.update({mm.start(0): mm.end(0)})
                for j in sorted(ad):
                    if j < bb.start():
                        a = j
                        continue
                if a > 0:
                    insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                    insuredname = insuredname.sub('', sentences2[ad[a]:bb.start()])
                    insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                    if len(insuredname) > 15:
                        insuredname = insuredname
                        return addresses[0], insuredname.strip()
                    else:
                        for jj in sorted(ad):
                            if jj < a:
                                b = jj
                                continue
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences2[ad[b]:bb.start()])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        return addresses[0], insuredname.replace('Insured', '   ')

        elif len(addresses) > 1:  # Multiple addresses found
            for aa in addresses:
                if re.search(aa, sentences2):
                    bb = re.search(aa, sentences2)
                    ab.update({bb.start(): bb.end()})

            for i in sorted(ab):
                if i > istartpos.start():  # address found after Insured Keyword
                    finaladdress = sentences2[i:ab[i]]
                    cnt = re.findall('insured', sentences2.lower())
                    if len(cnt) == 1:
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences2[istartpos.end():i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                    else:
                        for mm in re.finditer('insured', sen):
                            ad.update({mm.start(0): mm.end(0)})
                        for j in sorted(ad):
                            if j < i:
                                a = j
                                continue
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences2[ad[a]:i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        if len(insuredname) < 15:
                            insuredname = insuredname
                            return finaladdress, insuredname.strip()
                        else:
                            for jj in sorted(ad):
                                if jj < a:
                                    b = jj
                                    continue
                        return finaladdress, insuredname.strip()

        ######################### Search For Applicant Name in String ################################

        for insentence in insuredsentences:  # Serach for applicant keyword
            sent = " ".join([words[0].lower() for words in insentence])  # string of words in sentence
            # sentences1 += " ".join([words[0] for words in insentence])
            if re.search('applicant', sent):
                sentences1 = " ".join([words[0] for words in insentence])
                continue
            istartpos = re.search('applicant', sentences1.lower())
            sentences1 += " ".join([words[0] for words in insentence])
            if istartpos is not None:
                insuredaddress = pyap.parse(sentences1[istartpos.start():len(sentences1)], country='US')
                if len(insuredaddress) != 0:
                    break
        if len(insuredaddress) == 1:
            for cc in insuredaddress:
                if re.search(cc.full_address, sentences1):
                    dd = re.search(cc.full_address, sentences1)
                    ac.update({dd.start(): dd.end()})
                    cnt = re.findall('applicant', sentences1.lower())
                    if len(cnt) == 1:
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences1[istartpos.end():dd.start()])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.,]', '', insuredname)
                        return insuredaddress[0].full_address, insuredname.strip()
                    else:
                        for mm in re.finditer('applicant', sentences1.lower()):
                            ad.update({mm.start(0): mm.end(0)})
                        for j in sorted(ad):
                            if j < ad.start():
                                a = j
                                continue
                    insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                    insuredname = insuredname.sub('', sentences1[ad[a]:ac.start()])
                    insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                    if len(insuredname) > 15:
                        insuredname = insuredname
                        return addresses[0].full_address, insuredname.strip()
                    else:
                        for jj in sorted(ad):
                            if jj < a:
                                b = jj
                                continue
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences1[ad[b]:ac.start()])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        return addresses, insuredname.replace('Applicant', '').strip()

        elif len(insuredaddress) > 1:  # Multiple addresses found
            for aa in insuredaddress:
                if re.search(aa.full_address, sentences1):
                    bb = re.search(aa.full_address, sentences1)
                    ab.update({bb.start(): bb.end()})

            for i in sorted(ab):
                if i > istartpos.start():  # address found after Insured Keyword
                    finaladdress = sentences1[i:ab[i]]
                    cnt = re.findall('applicant', sentences1.lower())
                    if len(cnt) == 1:
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences1[istartpos.end():i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        return finaladdress, insuredname.strip()
                    else:
                        for mm in re.finditer('applicant', sen):
                            ad.update({mm.start(0): mm.end(0)})
                        for j in sorted(ad):
                            if j < i:
                                a = j
                                continue
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', sentences1[ad[a]:i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        if len(insuredname) < 15:
                            insuredname = insuredname
                            return finaladdress, insuredname.strip()
                        else:
                            for jj in sorted(ad):
                                if jj < a:
                                    b = jj
                                    continue
                        return finaladdress, insuredname.strip()

        ####################### Search For Insured Name and address in all documents by using Regex +++++++++++++++++++++

        if re.search('insured', inputstring.lower()):
            istartpos = re.search('insured', inputstring.lower())
            if istartpos is not None:
                addresses = re.findall(pattr, inputstring[istartpos.start():len(inputstring)])
                if len(addresses) == 0:
                    addresses = re.findall(pattr1, inputstring[istartpos.start():len(inputstring)])

        if len(alladdress) == 1:
            # istartpos = re.search('insured', inputstring.lower())
            bb = re.search(alladdress[0].full_address, inputstring)
            if bb is not None:
                ab.update({bb.start(): bb.end()})
            cnt = re.findall('insured', inputstring.lower())
            if len(cnt) == 1:
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', inputstring[istartpos.end():bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.,]', '', insuredname)
                return addresses[0], insuredname.strip()
            else:
                for mm in re.finditer('insured', sen):
                    ad.update({mm.start(0): mm.end(0)})
                for j in sorted(ad):
                    if j < bb.start():
                        a = j
                        continue
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', inputstring[ad[a]:bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                if len(insuredname) < 15:
                    insuredname = insuredname
                    return alladdress[0], insuredname.strip()
                else:
                    for jj in sorted(ad):
                        if jj < a:
                            b = jj
                            continue
                    insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                    insuredname = insuredname.sub('', inputstring[ad[b]:bb.start()])
                    insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                    return alladdress[0], insuredname.replace('Insured', '').strip()

        elif len(addresses) > 1:  # Multiple addresses found
            for aa in addresses:
                if re.search(aa, inputstring):
                    bb = re.search(aa, inputstring)
                    ab.update({bb.start(): bb.end()})

            for i in sorted(ab):
                if i > istartpos.start():  # address found after Insured Keyword
                    finaladdress = sentences1[i:ab[i]]
                    cnt = re.findall('insured', inputstring.lower())
                    if len(cnt) == 1:
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', inputstring[istartpos.end():i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                    else:
                        for mm in re.finditer('insured', sen):
                            ad.update({mm.start(0): mm.end(0)})
                        for j in sorted(ad):
                            if j < i:
                                a = j
                                continue
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', inputstring[ad[a]:i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        if len(insuredname) < 15:
                            insuredname = insuredname
                            return finaladdress, insuredname.strip()
                        else:
                            for jj in sorted(ad):
                                if jj < a:
                                    b = jj
                                    continue
                        return finaladdress, insuredname.strip()

        ####################### Search For Insured Name in all documents by using Py.Parse +++++++++++++++++++++

        if re.search('insured', inputstring.lower()):
            istartpos = re.search('insured', inputstring.lower())
            alladdress = pyap.parse(inputstring, country='US')

        if len(alladdress) == 1:
            # istartpos = re.search('insured', inputstring.lower())
            bb = re.search(alladdress[0].full_address, inputstring)
            if bb is not None:
                ab.update({bb.start(): bb.end()})
            cnt = re.findall('insured', inputstring.lower())
            if len(cnt) == 1:
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', inputstring[istartpos.end():bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.,]', '', insuredname)
                return addresses[0].full_address, insuredname.strip()
            else:
                for mm in re.finditer('insured', sen):
                    ad.update({mm.start(0): mm.end(0)})
                for j in sorted(ad):
                    if j < bb.start():
                        a = j
                        continue
                insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                insuredname = insuredname.sub('', inputstring[ad[a]:bb.start()])
                insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                if len(insuredname) < 15:
                    insuredname = insuredname
                    return alladdress[0], insuredname.strip()
                else:
                    for jj in sorted(ad):
                        if jj < a:
                            b = jj
                            continue
                    insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                    insuredname = insuredname.sub('', inputstring[ad[b]:bb.start()])
                    insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                    return alladdress[0], insuredname.replace('Insured', '').strip()

        elif len(addresses) > 1:  # Multiple addresses found
            for aa in addresses:
                if re.search(aa, inputstring):
                    bb = re.search(aa, inputstring)
                    ab.update({bb.start(): bb.end()})

            for i in sorted(ab):
                if i > istartpos.start():  # address found after Insured Keyword
                    finaladdress = sentences1[i:ab[i]]
                    cnt = re.findall('insured', inputstring.lower())
                    if len(cnt) == 1:
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', inputstring[istartpos.end():i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                    else:
                        for mm in re.finditer('insured', sen):
                            ad.update({mm.start(0): mm.end(0)})
                        for j in sorted(ad):
                            if j < i:
                                a = j
                                continue
                        insuredname = re.compile(re.escape('Address'), re.IGNORECASE)
                        insuredname = insuredname.sub('', inputstring[ad[a]:i])
                        insuredname = re.sub('[^a-zA-Z0-9 \n.]', '', insuredname)
                        if len(insuredname) < 15:
                            insuredname = insuredname
                            return finaladdress, insuredname.strip()
                        else:
                            for jj in sorted(ad):
                                if jj < a:
                                    b = jj
                                    continue
                        return finaladdress, insuredname.strip()
    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_brokeraddress(inputstring):
    brokeraddresses = []
    ab = {}
    sentences2 = ""
    startpos = 0
    finalbrokeraddr = ""
    pattr = '[\d]{1,5} [\w]+.*,[\s]+[A-Z]{2} \d{5}[-]*[\d]*(?= |$)'
    try:
        brokersentences = nltk.sent_tokenize(inputstring)
        brokersentences = [nltk.word_tokenize(sent) for sent in brokersentences]  # Tokenize the individual lines
        brokersentences = [nltk.pos_tag(sent) for sent in brokersentences]

        for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
            if re.search('marsh', sen):
                sentences2 = " ".join([words[0] for words in brokersentence])
                startpos = re.search('marsh', sentences2.lower())
                marshcount = re.findall('marsh', sentences2.lower())
                if len(sentences2) > (startpos.end() + 100) & len(marshcount) == 1:
                    brokeraddresses = pyap.parse(sentences2[startpos.start():startpos.end() + 100], country='US')
                else:
                    brokeraddresses = pyap.parse(sentences2[startpos.start():len(sentences2)], country='US')
                if len(brokeraddresses) != 0:
                    break
        if len(brokeraddresses) > 0:
            for aa in brokeraddresses:
                if re.search(aa.full_address, sentences2):
                    bb = re.search(aa.full_address, sentences2)
                    ab.update({bb.start(): bb.end()})

            for i in sorted(ab):
                if i > startpos.start():
                    finalbrokeraddr = sentences2[i:ab[i]]
                    return finalbrokeraddr

            ########################## Fond Using Regex #####################

        for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
            if re.search('marsh', sen):
                sentences2 = " ".join([words[0] for words in brokersentence])
                continue
            startpos = re.search('marsh', sentences2.lower())
            sentences2 += " ".join([words[0] for words in brokersentence])
            brokeraddresses = re.findall(pattr, sentences2[startpos.start():len(sentences2)])

            if len(brokeraddresses) != 0:
                return brokeraddresses
            else:
                brokeraddresses = pyap.parse(inputstring, country='US')
                return brokeraddresses
    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_policy_number(inputstring):
    global sentences2
    aa = []
    ac = []
    bb = []
    pattr = '(?:^|(?<= ))[A-Z0-9]+[\s]*[\d]{0,2}(?= |$)'
    pattr1 = '(?:^|(?<= ))[A-Z]+(?= |$)'
    pattr2 = '(?:^|(?<= ))[0-9]+(?= |$)'
    pattr3 = '[\d]{2}[-][\d]{3}[-][\d]{2}[-][\d]{2}'
    pattr4 = '(?:^|(?<= ))[A-Z]+[\s]*[\d]+[-][\d]{0,2}(?= |$)'  # 'SPR 4888535-08'
    pattr5 = '(?:^|(?<= ))[A-Z]+[-][A-Z0-9]+[-][A-Z0-9]+[-][A-Z]+[-][\d]{0,4}(?= |$)'
    pattr6 = '(?:^|(?<= ))[\d]{9}(?= |$)'  # 002867402
    pattr7 = '[A-Z0-9]+[\d]+[.][\d]{0,2}'  # MPL1960782.17
    pattr8 = '(?:^|(?<= ))[A-Z]+[\s]*[\d]{7}[\s]*[\d]{0,2}(?= |$)'  # MTE 9034937 02
    try:
        brokersentences = nltk.sent_tokenize(inputstring)
        brokersentences = [nltk.word_tokenize(sent) for sent in brokersentences]  # Tokenize the individual lines
        brokersentences = [nltk.pos_tag(sent) for sent in brokersentences]

        for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
            if re.search('policy number', sen):
                startpos = re.search('policy number', sen)
                sentences2 = " ".join([words[0] for words in brokersentence])
                aa = re.findall(pattr, sentences2[startpos.start():len(sentences2)])
                if len(aa) != 0:
                    break

        if len(aa) != 0:
            for ab in aa:
                if re.search(pattr1, ab) or re.search(pattr2, ab.replace(" ", "")):
                    continue
                else:
                    ac.append(ab)
        if len(ac) != 0:
            return ac
        else:
            for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
                sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
                if re.search('policy number', sen):
                    startpos = re.search('policy number', sen)
                    bb = re.findall(pattr3, sentences2[startpos.start():len(sentences2)])
                if len(bb) != 0:
                    return bb

            for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
                sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
                if re.search('policy number', sen):
                    startpos = re.search('policy number', sen)
                    bb = re.findall(pattr4, sentences2[startpos.start():len(sentences2)])
                if len(bb) != 0:
                    return bb

            for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
                sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
                if re.search('policy number', sen):
                    startpos = re.search('policy number', sen)
                    bb = re.findall(pattr5, sentences2[startpos.start():len(sentences2)])
                if len(bb) != 0:
                    return bb

            for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
                sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
                if re.search('policy number', sen):
                    startpos = re.search('policy number', sen)
                    bb = re.findall(pattr6, sentences2[startpos.start():len(sentences2)])
                if len(bb) != 0:
                    return bb

            for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
                sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
                if re.search('policy number', sen):
                    startpos = re.search('policy number', sen)
                    bb = re.findall(pattr8, sentences2[startpos.start():len(sentences2)])
                if len(bb) != 0:
                    return bb

            for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
                sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
                if re.search('policy number', sen):
                    startpos = re.search('policy number', sen)
                    bb = re.findall(pattr7, sentences2[startpos.start():len(sentences2)])
                if len(bb) != 0:
                    return bb

        if len(ac) == 0 and len(bb) == 0:
            for brokersentence in brokersentences:  # find the index of the sentence where the degree is find and then analyse that sentence
                sen = " ".join([words[0].lower() for words in brokersentence])  # string of words in sentence
                if re.search('policy #', sen):
                    startpos = re.search('policy #', sen)
                    sentences2 = " ".join([words[0] for words in brokersentence])
                    aa = re.findall(pattr, sentences2)
                    if len(aa) != 0:
                        break

            if len(aa) != 0:
                for ab in aa:
                    if re.search(pattr1, ab) or re.search(pattr2, ab):
                        continue
                    else:
                        ac.append(ab)
                        return ac


    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_underwriter_Email(inputstring):
    try:
        pattr = '(?:^|(?<= ))[\w\.-]+[\s]*@[\s]*[\w\.-]+[com]'
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('underwriter', sen.lower()):
                # result = re.search('underwriter', sen.lower())
                email = re.findall(pattr, sen, re.IGNORECASE)
                if email:
                    try:
                        return "".join(email[0].split())
                    except IndexError:
                        return None


    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_underwriter_contact(inputstring):
    try:
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('underwriter', sen.lower()):
                for match in phonenumbers.PhoneNumberMatcher(sen, "US"):
                    return phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL)

    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_underwriter_name(inputstring, matcher):
    try:
        underwriter_name = ""
        result = []
        grammar = ('CHUNK: {<NNP><NNP>}')
        cp = nltk.RegexpParser(grammar)
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        nlp = spacy.load('en')
        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('\\bunderwriter\\b', sen.lower()):
                state = nltk.sent_tokenize(sen)
                state = [nltk.word_tokenize(sent) for sent in state]
                state = [nltk.pos_tag(sent) for sent in state]
                for sent in state:
                    tree = cp.parse(sent)
                    for subtree in tree.subtrees():
                        if subtree.label() == 'CHUNK':
                            result.append(
                                str(subtree).replace('CHUNK', '').replace('/NNP', '').replace('(', '').replace(')',
                                                                                                               '').strip())
                            doc = nlp(str(result))
                            for en in doc.ents:
                                if en.label_ == 'PERSON':
                                    underwriter_name = en.text
                                    break

                doc = nlp(underwriter_name)
                for en in doc.ents:
                    if en.label_ == "PERSON":
                        return underwriter_name

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('\\bunderwriter\\b', sen.lower()):
                aa = re.findall('\\bunderwriter\\b', sen.lower())
                if len(aa) < 10:
                    doc = nlp(sen)
                    for en in doc.ents:
                        if en.label_ == 'ORG':
                            return en.text

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('\\bunderwriter\\b', sen.lower()):
                doc = nlp(sen)
                for en in doc.ents:
                    if en.label_ == 'PERSON':
                        return en.text

    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_broker_name(inputstring, matcher):
    global doc, aa
    try:
        broker_name = ""
        broker_first_name=""
        result = []
        sentences2 =""
        grammar = ('CHUNK: {<NNP><NNP>}')
        cp = nltk.RegexpParser(grammar)
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        nlp = spacy.load('en')

        # ------------- Search by Dear keyword  -------------------

        for sent in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sentence = " ".join([words[0] for words in sent])  # string of words in sentence
            if re.search('dear', sentence.lower()):
                dear_pos = re.search('dear', sentence.lower())
                broker_first_name = str(sentence[dear_pos.end():]).split()[0]
                break

        if broker_first_name is not None and len(broker_first_name) >0:
            for sent in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
                sentence = " ".join([words[0] for words in sent])
                if re.search(broker_first_name.lower(), sentence.lower()):
                    dear_pos = re.search(broker_first_name.lower(), sentence.lower())
                    aa = str(sentence[dear_pos.end():]).split()[0]
                    break
            return str(broker_first_name + " "+ aa).strip()

        # ------------------ Search for Attn keyword------------------------------------
        for sent in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sentence = " ".join([words[0] for words in sent])  # string of words in sentence
            if re.search('attn', sentence.lower()):
                sentences2 = " ".join([words[0] for words in sent])
                continue
            sentences2 = sentences2 + " "+sentence
            if re.search('attn', sentences2.lower()):
                insensitive_hippo = re.compile(re.escape('broker'), re.IGNORECASE)
                sen1 = insensitive_hippo.sub('', sentences2)
                state = nltk.sent_tokenize(sen1)
                state = [nltk.word_tokenize(sent) for sent in state]
                state = [nltk.pos_tag(sent) for sent in state]
                for sent in state:
                    tree = cp.parse(sent)
                    for subtree in tree.subtrees():
                        if subtree.label() == 'CHUNK':
                            result.append(
                            str(subtree).replace('CHUNK', '').replace('/NNP', '').replace('(', '').replace(')',
                                                                                                     '').strip())
                            doc = nlp(str(result))
                            for en in doc.ents:
                                if en.label_ == 'PERSON':
                                    broker_name = en.text
                                    break

                doc1 = nlp(broker_name)
                for en in doc1.ents:
                    if en.label_ == "PERSON":
                        return broker_name.replace('From', '').replace('\'', '').strip()


        # ------------- Search by Person Name using NLTK and Spacy keyword  ------------------

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('marsh', sen.lower()):
                # result = re.search('marsh',sen.lower())
                insensitive_hippo = re.compile(re.escape('broker'), re.IGNORECASE)
                sen1 = insensitive_hippo.sub('', sen)
                state = nltk.sent_tokenize(sen1)
                state = [nltk.word_tokenize(sent) for sent in state]
                state = [nltk.pos_tag(sent) for sent in state]
                for sent in state:
                    tree = cp.parse(sent)
                    for subtree in tree.subtrees():
                        if subtree.label() == 'CHUNK':
                            result.append(
                                str(subtree).replace('CHUNK', '').replace('/NNP', '').replace('(', '').replace(')',
                                                                                                               '').strip())
                            doc = nlp(str(result))

                for en in doc.ents:
                    if en.label_ == 'PERSON':
                        broker_name = en.text
                        break

                doc1 = nlp(broker_name)
                for en in doc1.ents:
                    if en.label_ == "PERSON":
                        return broker_name
        # ------------------------------ If Spacy Not able to find person name the select first NNP before marsh keyword------------------

        ''''for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('marsh', sen.lower()):
                result1 = re.search('marsh', sen.lower())
                insensitive_hippo = re.compile(re.escape('broker'), re.IGNORECASE)
                sen1 = insensitive_hippo.sub('', sen[:result1.start()])
                state = nltk.sent_tokenize(sen1)
                state = [nltk.word_tokenize(sent) for sent in state]
                state = [nltk.pos_tag(sent) for sent in state]
                for sent in state:
                    tree = cp.parse(sent)
                    for subtree in tree.subtrees():
                        if subtree.label() == 'CHUNK':
                            result2.append(
                                str(subtree).replace('CHUNK', '').replace('/NNP', '').replace('(', '').replace(')',
                                                                                                               '').strip())
                            # aa = len(result)
                return result2.pop()'''''

    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_waiting_time(inputstring):
    try:
        pattr = '(?:^|(?<= ))[\d]{1,2}[\s]*[H|D]'
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('waiting', sen.lower()):
                result = re.search('waiting', sen.lower())
                aa = re.findall(pattr, sen[result.end():])
                if aa is not None and len(aa) >0:
                    return aa[0]


    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_broker_state(broker_address):
    try:
        cc=""
        '''' places = GeoText(broker_address)
        if places.cities is not None and len(places.cities)> 1:
            city_name=places.cities[0]
            if str(city_name).lower() is 'york':
                return 'New York'
            else:return city_name
        else:
            return None'''
        bb = usaddress.parse(broker_address)
        for aa in bb:
            if str(aa).find('PlaceName') != -1:
                cc += ' ' + str(aa).replace('\'', '').replace('\'', '').replace('PlaceName', '').replace(',',
                                                                                                     '').replace(
                '(', '').replace(')', '').strip()
        return cc.strip()

    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_insured_state(insured_address):
    try:
        cc=""
        '''places = GeoText(insured_address)
        if places.cities is not None and len(places.cities) > 1:
            city_name = places.cities[0]
            if str(city_name).lower() is 'york':
                return 'New York'
            else:
                return city_name
        else:
            return None'''
        bb = usaddress.parse(insured_address)
        for aa in bb:
            if str(aa).find('PlaceName') != -1:
                cc += ' ' + str(aa).replace('\'', '').replace('\'', '').replace('PlaceName', '').replace(',','').replace(
                    '(', '').replace(')', '').strip()
        return cc.strip()

    except Exception as e:
        print(traceback.format_exc())
        print(e)


def extract_policy_form(inputstring):
    try:
        pattr = '(?:^|(?<= ))[\d]{1,2}[\s]*[H|D]'
        sentences = nltk.sent_tokenize(inputstring)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]  # Tokenize the individual lines
        sentences = [nltk.pos_tag(sent) for sent in sentences]

        for sentence in sentences:  # find the index of the sentence where the degree is find and then analyse that sentence
            sen = " ".join([words[0] for words in sentence])  # string of words in sentence
            if re.search('policy form', sen.lower()):
                result = re.search('policy form', sen.lower())
                aa = re.findall(pattr, sen[result.end():])
                if aa is not None:
                    return aa[0]


    except Exception as e:
        print(traceback.format_exc())
        print(e)
