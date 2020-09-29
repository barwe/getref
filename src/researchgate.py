from bs4 import BeautifulSoup

from .ref_base import RefBase

RESEARCH_GATE_LINKER = (' ', '%20')
COLON_REPLACER = (':', '%3A')

class ResearchGate(RefBase):
    
    def __init__(self, **kwargs):
        RefBase.__init__(self)
        self.ref_type = kwargs.get('ref_type', 'ris')
        self.output_dir = kwargs.get('output_dir', 'References')
        self.verbose = kwargs.get('verbose', True)
        
        self.querier = [RESEARCH_GATE_LINKER, COLON_REPLACER]
        
    def parse(self, title):
        site = 'https://www.researchgate.net/'
        querying_title = self.to_qstr(title)
        search_engine = site + 'search/publication?q={}'
        search_url = search_engine.format(querying_title)
        response = self.request(search_url)
        bs = BeautifulSoup(response.text, 'lxml')
        
        main = bs.select_one('div[class="js-items"]')\
                 .select_one('div[class="nova-o-stack__item"]')\
                 .select_one('a[class="nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare"]')
        
        title = main.text
        ID = main.get('href').split('_')[0].split('/')[1]
        
        download_params = 'fileType=RIS&citation=citation&publicationUid=%s' % ID 
        download_engine = site + 'lite.publication.PublicationDownloadCitationModal.downloadCitation.html'
        download_url = download_engine + '?' + download_params
        
        return title, download_url