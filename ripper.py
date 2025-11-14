#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نازع البوابات - Gateway Ripper
أداة متقدمة لتحليل بوابات الدفع

تكتشف تلقائياً بوابات الدفع على المواقع وتولد
كود Python جاهز للاستخدام المباشر.

المطور: فريق Gateway-Ripper
الرخصة: MIT
"""

import sys
import argparse
import warnings
from pathlib import Path

# تعطيل تحذيرات SSL
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent))

from core import WebCrawler, GatewayAnalyzer, DataExtractor
from modules import get_gateway_handler
from utils import logger, Validator
from colorama import Fore, Style, init

# تهيئة colorama
init(autoreset=True)

class GatewayRipper:
    """التطبيق الرئيسي لنازع البوابات"""
    
    def __init__(self, target_url, verbose=False, output_file=None):
        """
        تهيئة نازع البوابات
        
        المعاملات:
            target_url (str): رابط الموقع المستهدف
            verbose (bool): تفعيل الوضع التفصيلي
            output_file (str): مسار ملف الحفظ للكود المولد
        """
        self.target_url = Validator.normalize_url(target_url)
        self.verbose = verbose
        self.output_file = output_file
        self.results = {}
        
        # تحديث مستوى التفاصيل
        logger.verbose = verbose
    
    def print_banner(self):
        """طباعة شعار التطبيق"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ███╗   ██╗ █████╗ ███████╗███████╗     █████╗ ██╗              ║
║   ████╗  ██║██╔══██╗╚══███╔╝██╔════╝    ██╔══██╗██║              ║
║   ██╔██╗ ██║███████║  ███╔╝ █████╗      ███████║██║              ║
║   ██║╚██╗██║██╔══██║ ███╔╝  ██╔══╝      ██╔══██║██║              ║
║   ██║ ╚████║██║  ██║███████╗███████╗    ██║  ██║███████╗         ║
║   ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚══════╝         ║
║                                                                   ║
║   ██████╗  █████╗ ██╗    ██╗ █████╗ ██████╗  █████╗ ████████╗   ║
║   ██╔══██╗██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝   ║
║   ██████╔╝███████║██║ █╗ ██║███████║██████╔╝███████║   ██║      ║
║   ██╔══██╗██╔══██║██║███╗██║██╔══██║██╔══██╗██╔══██║   ██║      ║
║   ██████╔╝██║  ██║╚███╔███╔╝██║  ██║██████╔╝██║  ██║   ██║      ║
║   ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝      ║
║                                                                   ║
║                    💳 نــــازع البــوابــات 💳                    ║
║                                                                   ║
║              🔓 أداة متقدمة لاستخراج بوابات الدفع 🔓             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}⚡ الإصدار: 1.0.0{Style.RESET_ALL}
{Fore.YELLOW}🎯 الوظيفة: استخراج بوابات الدفع تلقائياً وتوليد كود جاهز{Style.RESET_ALL}
{Fore.RED}⚠️  تحذير: للاستخدام التعليمي والمصرح به فقط{Style.RESET_ALL}
"""
        print(banner)
    
    def validate_target(self):
        """
        التحقق من صحة الرابط المستهدف
        
        المخرجات:
            bool: True إذا كان صحيحاً، False خلاف ذلك
        """
        if not Validator.is_valid_url(self.target_url):
            logger.error(f"رابط غير صحيح: {self.target_url}")
            return False
        
        logger.info(f"تم التحقق من الهدف: {self.target_url}")
        return True
    
    def crawl_target(self):
        """
        الزحف إلى الموقع المستهدف
        
        المخرجات:
            dict: نتائج الزحف أو None عند الفشل
        """
        logger.banner("المرحلة 1: الزحف إلى الموقع")
        
        crawler = WebCrawler(self.target_url)
        crawl_results = crawler.crawl()
        
        if not crawl_results:
            logger.error("فشل الزحف إلى الموقع المستهدف")
            return None
        
        self.results['crawl'] = crawl_results
        return crawl_results
    
    def analyze_content(self, content):
        """
        تحليل المحتوى للبحث عن بوابات الدفع
        
        المعاملات:
            content (str): المحتوى المراد تحليله
            
        المخرجات:
            dict: نتائج التحليل أو None عند الفشل
        """
        logger.banner("المرحلة 2: كشف بوابات الدفع")
        
        analyzer = GatewayAnalyzer(content)
        analysis = analyzer.analyze()
        
        if not analysis['detected_gateways']:
            logger.error("لم يتم العثور على أي بوابات دفع في الموقع المستهدف")
            logger.info("قد لا يحتوي هذا الموقع على نظام دفع، أو يستخدم تطبيقاً مخصصاً")
            return None
        
        self.results['analysis'] = analysis
        return analysis
    
    def extract_configuration(self, content, gateway_name):
        """
        استخراج الإعدادات الإضافية
        
        المعاملات:
            content (str): المحتوى المراد الاستخراج منه
            gateway_name (str): اسم البوابة الرئيسية
            
        المخرجات:
            dict: الإعدادات المستخرجة
        """
        logger.banner("المرحلة 3: استخراج الإعدادات")
        
        extractor = DataExtractor(content)
        config = extractor.extract_all(gateway_name)
        
        self.results['config'] = config
        return config
    
    def generate_code(self, gateway_name, keys, config):
        """
        توليد كود Python للبوابة
        
        المعاملات:
            gateway_name (str): اسم البوابة
            keys (list): مفاتيح API
            config (dict): الإعدادات
            
        المخرجات:
            str: الكود المولد أو None عند الفشل
        """
        logger.banner("المرحلة 4: توليد الكود")
        
        handler = get_gateway_handler(gateway_name, keys, config)
        
        if not handler:
            logger.error(f"لا يوجد مولد كود متاح لـ {gateway_name}")
            logger.info(f"البوابات المدعومة: stripe, braintree")
            return None
        
        code = handler.generate_code()
        self.results['code'] = code
        
        logger.success(f"تم توليد الكود بنجاح لـ {gateway_name.upper()}")
        return code
    
    def display_results(self):
        """عرض نتائج التحليل"""
        logger.banner("نتائج التحليل")
        
        analysis = self.results.get('analysis', {})
        primary = analysis.get('primary_gateway')
        
        if not primary:
            return
        
        # عرض البوابات المكتشفة
        print(f"{Fore.GREEN}✓ البوابة الرئيسية:{Style.RESET_ALL} {primary['name'].upper()}")
        print(f"{Fore.GREEN}✓ درجة الثقة:{Style.RESET_ALL} {primary['score']}")
        
        # عرض المفاتيح المستخرجة
        if primary['keys']:
            print(f"\n{Fore.CYAN}المفاتيح المستخرجة:{Style.RESET_ALL}")
            for key in primary['keys']:
                # إخفاء المفتاح للأمان
                masked = key[:12] + '*' * (len(key) - 16) + key[-4:]
                print(f"  • {masked}")
        
        # عرض البوابات الأخرى المكتشفة
        other_gateways = [g for g in analysis['detected_gateways'] if g['name'] != primary['name']]
        if other_gateways:
            print(f"\n{Fore.YELLOW}بوابات أخرى مكتشفة:{Style.RESET_ALL}")
            for gateway in other_gateways:
                print(f"  • {gateway['name'].upper()} (الدرجة: {gateway['score']})")
        
        # عرض الإعدادات
        config = self.results.get('config', {})
        if config.get('currencies'):
            print(f"\n{Fore.CYAN}العملات المكتشفة:{Style.RESET_ALL} {', '.join(config['currencies'])}")
        
        logger.separator()
    
    def display_code(self):
        """عرض الكود المولد"""
        code = self.results.get('code')
        
        if not code:
            return
        
        logger.banner("الكود المولد (Python)")
        print(f"{Fore.GREEN}{code}{Style.RESET_ALL}")
        logger.separator()
        
        # الحفظ في ملف إذا تم تحديده
        if self.output_file:
            try:
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    f.write(code)
                logger.success(f"تم حفظ الكود في: {self.output_file}")
            except Exception as e:
                logger.error(f"فشل حفظ الكود: {e}")
    
    def run(self):
        """تنفيذ عملية التحليل الكاملة"""
        self.print_banner()
        
        # التحقق من الهدف
        if not self.validate_target():
            return False
        
        # المرحلة 1: الزحف
        crawl_results = self.crawl_target()
        if not crawl_results:
            return False
        
        # المرحلة 2: التحليل
        content = crawl_results['all_content']
        analysis = self.analyze_content(content)
        if not analysis:
            return False
        
        # الحصول على البوابة الرئيسية
        primary = analysis['primary_gateway']
        gateway_name = primary['name']
        keys = primary['keys']
        
        if not keys:
            logger.warning(f"لم يتم العثور على مفاتيح API لـ {gateway_name}")
            logger.info("قد يستخدم الموقع إدارة المفاتيح من جانب الخادم")
        
        # المرحلة 3: استخراج الإعدادات
        config = self.extract_configuration(content, gateway_name)
        
        # المرحلة 4: توليد الكود
        code = self.generate_code(gateway_name, keys, config)
        
        # عرض النتائج
        self.display_results()
        
        if code:
            self.display_code()
            logger.banner("تعليمات الاستخدام")
            print(f"{Fore.CYAN}1.{Style.RESET_ALL} انسخ الكود المولد أعلاه")
            print(f"{Fore.CYAN}2.{Style.RESET_ALL} احفظه في ملف Python (مثلاً: payment_processor.py)")
            print(f"{Fore.CYAN}3.{Style.RESET_ALL} ثبت المكتبات المطلوبة: pip install requests")
            print(f"{Fore.CYAN}4.{Style.RESET_ALL} استورد واستخدم الكلاس في مشروعك")
            print(f"\n{Fore.YELLOW}ملاحظة:{Style.RESET_ALL} استخدم دائماً بطاقات الاختبار!")
            print(f"{Fore.RED}⚠️  لا تستخدم أبداً أرقام بطاقات حقيقية بدون تصريح{Style.RESET_ALL}\n")
        
        return True


def main():
    """نقطة الدخول الرئيسية"""
    parser = argparse.ArgumentParser(
        description='نازع البوابات - أداة متقدمة لتحليل بوابات الدفع',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
أمثلة الاستخدام:
  python ripper.py --url https://example.com
  python ripper.py --url example.com --output payment.py
  python ripper.py --url https://shop.example.com --verbose

للمزيد من المعلومات، زر: https://github.com/yourusername/gateway-ripper
        '''
    )
    
    parser.add_argument(
        '-u', '--url',
        required=True,
        help='رابط الموقع المستهدف',
        metavar='الرابط'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='مسار ملف الحفظ للكود المولد',
        metavar='الملف'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='تفعيل الوضع التفصيلي'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='نازع البوابات v1.0.0'
    )
    
    args = parser.parse_args()
    
    # إنشاء وتشغيل نازع البوابات
    ripper = GatewayRipper(
        target_url=args.url,
        verbose=args.verbose,
        output_file=args.output
    )
    
    success = ripper.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
