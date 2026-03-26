import re
from bs4 import BeautifulSoup

class HTMLParser:
    @staticmethod
    def extract_forms(html):
        """Extract all forms from HTML with action, method, and input names"""
        soup = BeautifulSoup(html, 'html.parser')
        forms = []
        for form in soup.find_all('form'):
            action = form.get('action', '')
            method = form.get('method', 'get').upper()
            inputs = []
            for inp in form.find_all('input'):
                name = inp.get('name')
                if name:
                    inputs.append(name)
            forms.append({
                'action': action,
                'method': method,
                'inputs': inputs
            })
        return forms

    @staticmethod
    def extract_links(html):
        """Extract all href links from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            links.append(a['href'])
        return links

    @staticmethod
    def extract_scripts(html):
        """Extract inline JavaScript code"""
        soup = BeautifulSoup(html, 'html.parser')
        scripts = []
        for script in soup.find_all('script'):
            if script.string:
                scripts.append(script.string.strip())
        return scripts

    @staticmethod
    def extract_meta_refresh(html):
        """Extract meta refresh URL"""
        soup = BeautifulSoup(html, 'html.parser')
        meta = soup.find('meta', attrs={'http-equiv': 'refresh'})
        if meta and meta.get('content'):
            match = re.search(r'url=(.+)', meta['content'], re.I)
            if match:
                return match.group(1)
        return None