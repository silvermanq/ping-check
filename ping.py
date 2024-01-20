import subprocess
import re

# تابع برای ارسال پینگ و برگرفتن زمان‌ها
def ping_host(host, count):
    ping_command = ['ping', '-c', str(count), host]
    try:
        ping_output = subprocess.check_output(ping_command).decode('utf-8')
        ping_times = re.findall(r'time=(\d+\.\d+)', ping_output)
        ping_times = [float(time) for time in ping_times]
        return sum(ping_times) / len(ping_times) if ping_times else None  # Return average
    except subprocess.CalledProcessError:
        return None

# تعداد دفعات پینگ
number_of_pings = 6

# لیست آدرس‌های اولیه و ثانویه
primary_ips = ['5.126.0.179', '5.126.0.180']
secondary_ips = ['128.65.165.5', '185.231.115.179']

# متغیر برای کنترل پینگ همه ایپی‌ها به یکدیگر یا فقط متناظرها
ping_all = True  # به طور پیش‌فرض فقط نسبت‌ها بین آدرس‌های متناظر

# نتایج را در فایل بنویسید
with open('ping_results.txt', 'w') as file:
    if ping_all:
        # نظام کامل: هر آدرس IP اولیه به همه آدرس‌های IP ثانویه پینگ می‌شود
        for primary_ip in primary_ips:
            for secondary_ip in secondary_ips:
                avg_ping = ping_host(primary_ip, number_of_pings)
                file.write(f"Average ping from {primary_ip} to {secondary_ip} is: {avg_ping} ms\n")
    else:
        # نظام متناظر: هر آدرس IP اولیه فقط به آدرس متناظر ثانویه پینگ می‌شود
        for primary_ip, secondary_ip in zip(primary_ips, secondary_ips):
            avg_ping = ping_host(secondary_ip, number_of_pings)
            file.write(f"Average ping from {primary_ip} to {secondary_ip} is: {avg_ping} ms\n")
