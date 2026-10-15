from chaos import slow_database, break_dns, kill_services

EXPERIMENTS = {
    "slow_database": slow_database,
    "break_dns": break_dns,
    "kill_services": kill_services,
}


def run_experiment(name: str):
    if name not in EXPERIMENTS:
        raise ValueError(f"Unknown experiment: '{name}'")
    EXPERIMENTS[name].apply()
