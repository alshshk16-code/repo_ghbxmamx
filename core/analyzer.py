# -*- coding: utf-8 -*-
"""
وحدة المحلل
تكتشف بوابات الدفع وتستخرج مفاتيح API من المحتوى
"""

import re
from utils import logger, Validator

# بصمات بوابات الدفع
GATEWAY_FINGERPRINTS = {
    'stripe': {
        'domains': ['stripe.com', 'stripe.js', 'js.stripe.com'],
        'keywords': ['Stripe', 'stripe.createToken', 'stripe.createPaymentMethod', 'stripe.confirmCardPayment'],
        'key_pattern': r'(pk_(?:test|live)_[a-zA-Z0-9]{24,})',
        'priority': 1
    },
    'braintree': {
        'domains': ['braintreegateway.com', 'braintree-api.com', 'braintree.js'],
        'keywords': ['braintree', 'Braintree', 'braintree.client.create', 'braintree.hostedFields'],
        'key_pattern': r'["\']([a-zA-Z0-9_-]{20,})["\']',
        'priority': 2
    },
    'checkout': {
        'domains': ['checkout.com', 'checkout.js', 'cdn.checkout.com'],
        'keywords': ['Checkout', 'Frames', 'checkout.com', 'CheckoutKit'],
        'key_pattern': r'pk_[a-zA-Z0-9_-]{32,}',
        'priority': 3
    },
    'paypal': {
        'domains': ['paypal.com', 'paypalobjects.com', 'paypal.js'],
        'keywords': ['paypal', 'PayPal', 'paypal.Buttons', 'paypal.checkout'],
        'key_pattern': r'["\']([A-Z0-9_-]{60,80})["\']',
        'priority': 4
    },
    'square': {
        'domains': ['squareup.com', 'square.js', 'squareupsandbox.com'],
        'keywords': ['Square', 'square', 'SqPaymentForm', 'square.payments'],
        'key_pattern': r'sq0[a-z]{3}-[a-zA-Z0-9_-]{22,}',
        'priority': 5
    },
    'razorpay': {
        'domains': ['razorpay.com', 'checkout.razorpay.com'],
        'keywords': ['Razorpay', 'razorpay', 'rzp_'],
        'key_pattern': r'rzp_(test|live)_[a-zA-Z0-9]{14}',
        'priority': 6
    },
    'mollie': {
        'domains': ['mollie.com', 'mollie.js'],
        'keywords': ['Mollie', 'mollie', 'mollie.createToken'],
        'key_pattern': r'(test|live)_[a-zA-Z0-9]{30,}',
        'priority': 7
    }
}


class GatewayAnalyzer:
    """يحلل المحتوى لاكتشاف بوابات الدفع"""
    
    def __init__(self, content):
        """
        تهيئة المحلل
        
        المعاملات:
            content (str): محتوى الموقع (HTML + JS) للتحليل
        """
        self.content = content
        self.detected_gateways = []
        self.extracted_keys = {}
    
    def detect_gateways(self):
        """
        كشف جميع بوابات الدفع الموجودة في المحتوى
        
        المخرجات:
            list: قائمة بأسماء البوابات المكتشفة
        """
        logger.info("تحليل المحتوى للبحث عن بوابات الدفع...")
        
        for gateway_name, fingerprint in GATEWAY_FINGERPRINTS.items():
            score = 0
            
            # فحص النطاقات
            for domain in fingerprint['domains']:
                if domain.lower() in self.content.lower():
                    score += 3
                    logger.debug(f"تم العثور على نطاق {gateway_name}: {domain}")
            
            # فحص الكلمات المفتاحية
            for keyword in fingerprint['keywords']:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = re.findall(pattern, self.content)
                if matches:
                    score += len(matches)
                    logger.debug(f"تم العثور على كلمة مفتاحية {gateway_name}: {keyword} ({len(matches)} مرة)")
            
            # إذا كانت الدرجة عالية بما فيه الكفاية، اعتبرها مكتشفة
            if score >= 3:
                self.detected_gateways.append({
                    'name': gateway_name,
                    'score': score,
                    'priority': fingerprint['priority']
                })
                logger.success(f"تم اكتشاف البوابة: {gateway_name.upper()} (درجة الثقة: {score})")
        
        # الترتيب حسب الدرجة (الأعلى أولاً)
        self.detected_gateways.sort(key=lambda x: (-x['score'], x['priority']))
        
        if not self.detected_gateways:
            logger.warning("لم يتم اكتشاف أي بوابات دفع")
        else:
            logger.success(f"إجمالي البوابات المكتشفة: {len(self.detected_gateways)}")
        
        return [g['name'] for g in self.detected_gateways]
    
    def extract_keys(self, gateway_name=None):
        """
        استخراج مفاتيح API للبوابات المكتشفة
        
        المعاملات:
            gateway_name (str): بوابة محددة لاستخراج المفاتيح منها، أو None للكل
            
        المخرجات:
            dict: قاموس بأسماء البوابات والمفاتيح المستخرجة
        """
        if gateway_name:
            gateways_to_process = [gateway_name]
        else:
            gateways_to_process = [g['name'] for g in self.detected_gateways]
        
        logger.info("استخراج مفاتيح API...")
        
        for gateway in gateways_to_process:
            if gateway not in GATEWAY_FINGERPRINTS:
                continue
            
            pattern = GATEWAY_FINGERPRINTS[gateway]['key_pattern']
            matches = re.findall(pattern, self.content)
            
            if matches:
                # لـ Stripe، نحصل على tuples من مجموعات regex
                if gateway == 'stripe':
                    keys = [''.join(match) if isinstance(match, tuple) else match for match in matches]
                else:
                    keys = list(set(matches))  # إزالة التكرارات
                
                # التحقق من المفاتيح
                valid_keys = []
                for key in keys:
                    if gateway == 'stripe' and Validator.is_stripe_key(key):
                        valid_keys.append(key)
                    elif len(key) >= 20:  # فحص الطول الأساسي للبوابات الأخرى
                        valid_keys.append(key)
                
                if valid_keys:
                    self.extracted_keys[gateway] = valid_keys
                    logger.success(f"تم استخراج {len(valid_keys)} مفتاح لـ {gateway.upper()}")
                    for key in valid_keys:
                        # إخفاء المفتاح للأمان
                        masked_key = key[:12] + '*' * (len(key) - 16) + key[-4:]
                        logger.debug(f"  المفتاح: {masked_key}")
        
        if not self.extracted_keys:
            logger.warning("لم يتم استخراج أي مفاتيح API")
        
        return self.extracted_keys
    
    def get_primary_gateway(self):
        """
        الحصول على البوابة الرئيسية (الأكثر احتمالاً)
        
        المخرجات:
            dict: معلومات البوابة الرئيسية مع الاسم والمفاتيح
        """
        if not self.detected_gateways:
            return None
        
        primary = self.detected_gateways[0]
        gateway_name = primary['name']
        
        return {
            'name': gateway_name,
            'score': primary['score'],
            'keys': self.extracted_keys.get(gateway_name, [])
        }
    
    def analyze(self):
        """
        إجراء التحليل الكامل
        
        المخرجات:
            dict: نتائج التحليل
        """
        gateways = self.detect_gateways()
        keys = self.extract_keys()
        primary = self.get_primary_gateway()
        
        return {
            'detected_gateways': self.detected_gateways,
            'extracted_keys': keys,
            'primary_gateway': primary
        }
