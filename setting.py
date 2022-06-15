def setting_save(setting_data,app):
    birth_month, birth_day, voice, area, notice_step = setting_data
    month = birth_month.get()
    day = birth_day.get()    
    area = area.get()
    notice_step = notice_step.get()
    data = [month,day,voice,area,notice_step]
    with open('setting.txt', mode = 'w', encoding = 'utf-8') as f:
        for d in data:
            f.write(d+'\n')
    app.destroy()

def setting_load():
    with open('setting.txt', mode = 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    for i,line in enumerate(lines):
        lines[i]=line.replace('\n','')
    return lines
        
        


