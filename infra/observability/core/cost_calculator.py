from typing import List, Dict
from .models import IAInteraction, CostConfig

# Precios estimados por 1M de tokens (Mayo 2026)
PRICING_TABLE = {
    "gemini-1.5-pro": CostConfig(model_name="gemini-1.5-pro", input_cost_per_1k=0.0035, output_cost_per_1k=0.0105),
    "gemini-1.5-flash": CostConfig(model_name="gemini-1.5-flash", input_cost_per_1k=0.00035, output_cost_per_1k=0.00105),
    "gpt-4o": CostConfig(model_name="gpt-4o", input_cost_per_1k=0.005, output_cost_per_1k=0.015),
}

class CostCalculator:
    @staticmethod
    def calculate_interaction_cost(interaction: IAInteraction) -> float:
        config = PRICING_TABLE.get(interaction.model_id.lower())
        if not config:
            return 0.0
        
        input_cost = (interaction.prompt_tokens / 1000) * config.input_cost_per_1k
        output_cost = (interaction.completion_tokens / 1000) * config.output_cost_per_1k
        return input_cost + output_cost

    @staticmethod
    def analyze_logs(log_file_path: str) -> Dict:
        total_cost = 0.0
        total_tokens = 0
        success_count = 0
        fail_count = 0
        latencies = []
        
        try:
            with open(log_file_path, "r", encoding="utf-8") as f:
                for line in f:
                    data = IAInteraction.model_validate_json(line)
                    total_cost += CostCalculator.calculate_interaction_cost(data)
                    total_tokens += data.total_tokens
                    latencies.append(data.latency_ms)
                    if data.status == "success":
                        success_count += 1
                    else:
                        fail_count += 1
        except FileNotFoundError:
            return {"error": "Archivo no encontrado"}

        return {
            "total_estimated_cost": round(total_cost, 4),
            "total_tokens": total_tokens,
            "success_rate": round(success_count / (success_count + fail_count), 2) if (success_count + fail_count) > 0 else 0,
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0
        }
