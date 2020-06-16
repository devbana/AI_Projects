import BinderInformationExtractor.Binder_Parser as Binder_Parser
import time
#start = time.process_time()
data = Binder_Parser.BinderParser('C:\\Binders File\\AIG.doc').get_extracted_data()
print(data)
#print(time.process_time() - start)


