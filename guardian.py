import yaml
import sys
import logging

class TokenGuardian:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.settings = self.config['sentry_settings']
        self.pricing = self.config['pricing_table']
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - [Guardian] - %(message)s')

    def audit_cost(self, usage_data):
        """计算实时成本"""
        model = usage_data.get("model", "qwen-max")
        price = self.pricing.get(model, self.pricing['qwen-max'])
        
        cost = (usage_data['input_tokens'] / 1000000 * price['input']) + \
               (usage_data['output_tokens'] / 1000000 * price['output'])
        return round(cost, 4)

    def enforce_policy(self, current_total_cost):
        """执行熔断策略"""
        if current_total_cost >= self.settings['hard_limit']:
            logging.error(f"🚨 熔断触发！当前任务已消耗 {current_total_cost} {self.settings['currency']}，强行终止进程止损。")
            sys.exit(1) # 物理切断
        elif current_total_cost >= self.settings['soft_warning']:
            logging.warning(f"⚠️ 预算预警！当前消耗 {current_total_cost} {self.settings['currency']}，请检查逻辑。")