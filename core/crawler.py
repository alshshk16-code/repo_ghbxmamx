# -*- coding: utf-8 -*-
"""
وحدة الزاحف
تجلب وتستخرج ملفات JavaScript وأصول الدفع من الموقع المستهدف
"""

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from fake_useragent import UserAgent
from utils import logger

class WebCrawler:
    """يزحف إلى الموقع المستهدف ويستخرج ملفات JavaScript"""
    
    def __init__(self, target_url, timeout=30):
        """
        تهيئة الزاحف
        
        المعاملات:
            target_url (str): رابط الموقع المستهدف
            timeout (int): مهلة الطلب بالثواني
        """
        self.target_url = target_url
        self.timeout = timeout
        self.session = requests.Session()
        self.ua = UserAgent()
        self.js_files = []
        self.html_content = ""
        
        # تعيين الرؤوس
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def fetch_page(self):
        """
        جلب صفحة HTML الرئيسية
        
        المخرجات:
            bool: True إذا نجح، False خلاف ذلك
        """
        try:
            logger.info(f"جلب الهدف: {self.target_url}")
            response = self.session.get(self.target_url, timeout=self.timeout, verify=False)
            response.raise_for_status()
            
            self.html_content = response.text
            logger.success(f"تم جلب الصفحة بنجاح ({len(self.html_content)} بايت)")
            return True
            
        except requests.exceptions.Timeout:
            logger.error("انتهت مهلة الطلب")
            return False
        except requests.exceptions.ConnectionError:
            logger.error("خطأ في الاتصال - تحقق من الإنترنت أو الرابط المستهدف")
            return False
        except requests.exceptions.HTTPError as e:
            logger.error(f"خطأ HTTP: {e}")
            return False
        except Exception as e:
            logger.error(f"خطأ غير متوقع: {e}")
            return False
    
    def extract_js_files(self):
        """
        استخراج جميع روابط ملفات JavaScript من HTML
        
        المخرجات:
            list: قائمة بروابط ملفات JavaScript
        """
        if not self.html_content:
            logger.warning("لا يوجد محتوى HTML للتحليل")
            return []
        
        logger.info("استخراج ملفات JavaScript...")
        soup = BeautifulSoup(self.html_content, 'lxml')
        
        # البحث عن جميع وسوم script
        script_tags = soup.find_all('script')
        
        for script in script_tags:
            # ملفات JS خارجية
            if script.get('src'):
                js_url = urljoin(self.target_url, script['src'])
                self.js_files.append({
                    'url': js_url,
                    'type': 'external',
                    'content': None
                })
            # JS مضمن
            elif script.string:
                self.js_files.append({
                    'url': self.target_url,
                    'type': 'inline',
                    'content': script.string
                })
        
        logger.success(f"تم العثور على {len(self.js_files)} مصدر JavaScript")
        return self.js_files
    
    def fetch_js_content(self):
        """
        تنزيل محتوى جميع ملفات JavaScript الخارجية
        
        المخرجات:
            list: قائمة بملفات JS مع المحتوى
        """
        logger.info("تنزيل ملفات JavaScript...")
        
        downloaded = 0
        for js_file in self.js_files:
            if js_file['type'] == 'external':
                try:
                    response = self.session.get(js_file['url'], timeout=self.timeout, verify=False)
                    if response.status_code == 200:
                        js_file['content'] = response.text
                        downloaded += 1
                        logger.debug(f"تم التنزيل: {js_file['url']}")
                except Exception as e:
                    logger.debug(f"فشل تنزيل {js_file['url']}: {e}")
                    continue
        
        logger.success(f"تم تنزيل {downloaded} ملف JavaScript")
        return self.js_files
    
    def get_all_content(self):
        """
        الحصول على جميع محتوى JavaScript (مضمن + خارجي) كنص واحد
        
        المخرجات:
            str: محتوى JavaScript المجمع
        """
        all_js = self.html_content + "\n\n"
        
        for js_file in self.js_files:
            if js_file['content']:
                all_js += f"\n\n/* المصدر: {js_file['url']} */\n"
                all_js += js_file['content']
        
        return all_js
    
    def crawl(self):
        """
        تنفيذ عملية الزحف الكاملة
        
        المخرجات:
            dict: نتائج الزحف مع محتوى HTML و JS
        """
        if not self.fetch_page():
            return None
        
        self.extract_js_files()
        self.fetch_js_content()
        
        return {
            'url': self.target_url,
            'html': self.html_content,
            'js_files': self.js_files,
            'all_content': self.get_all_content()
        }
