# -*- coding: utf-8 -*-
"""
أداة السجلات لنازع البوابات
توفر مخرجات ملونة للطرفية مع مستويات سجل مختلفة
"""

from colorama import Fore, Style, init
from datetime import datetime

# تهيئة colorama
init(autoreset=True)

class Logger:
    """مسجل مخصص مع مخرجات ملونة"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def _timestamp(self):
        """الحصول على الطابع الزمني الحالي"""
        return datetime.now().strftime("%H:%M:%S")
    
    def info(self, message):
        """سجل مستوى معلومات"""
        print(f"{Fore.CYAN}[معلومات]{Style.RESET_ALL} [{self._timestamp()}] {message}")
    
    def success(self, message):
        """سجل مستوى نجاح"""
        print(f"{Fore.GREEN}[نجح]{Style.RESET_ALL} [{self._timestamp()}] {message}")
    
    def warning(self, message):
        """سجل مستوى تحذير"""
        print(f"{Fore.YELLOW}[تحذير]{Style.RESET_ALL} [{self._timestamp()}] {message}")
    
    def error(self, message):
        """سجل مستوى خطأ"""
        print(f"{Fore.RED}[خطأ]{Style.RESET_ALL} [{self._timestamp()}] {message}")
    
    def debug(self, message):
        """سجل مستوى تصحيح (يظهر فقط في الوضع التفصيلي)"""
        if self.verbose:
            print(f"{Fore.MAGENTA}[تصحيح]{Style.RESET_ALL} [{self._timestamp()}] {message}")
    
    def banner(self, text):
        """طباعة نص بارز"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{text.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def separator(self):
        """طباعة خط فاصل"""
        print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")

# نسخة عامة من المسجل
logger = Logger()
