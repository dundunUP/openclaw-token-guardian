from guardian import TokenGuardian
import time

def run_simulation():
    sentry = TokenGuardian()
    accumulated_cost = 0.0
    
    print("🚀 Token-Guardian 演示模式启动 (模拟 OpenClaw 任务流)...")
    
    # 模拟 15 次 Agent 迭代
    for i in range(1, 16):
        # 模拟每次消耗约 2 元的流量
        simulated_usage = {"model": "qwen-max", "input_tokens": 50000, "output_tokens": 20000}
        step_cost = sentry.audit_cost(simulated_usage)
        accumulated_cost += step_cost
        
        print(f"步骤 {i}: 本次花费 {step_cost} 元，累计总额 {round(accumulated_cost, 2)} 元")
        
        # 实时审计与熔断
        sentry.enforce_policy(accumulated_cost)
        time.sleep(0.5)

if __name__ == "__main__":
    run_simulation()