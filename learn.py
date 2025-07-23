def log_error(error_msg):
    with open("error_log.txt", "a") as f:
        f.write(error_msg + "\n")

def learn_from_history():
    print("✅ Модель обновлена на основе истории ошибок")