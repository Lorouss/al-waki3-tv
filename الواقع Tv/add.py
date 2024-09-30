import os
import sys
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, Canvas, Frame, Scrollbar, Toplevel, Listbox
from tkinter import font as tkFont

# الحصول على المسار الأساسي، يعتمد على كون البرنامج تم تشغيله من بيئة عادية أو من ملف EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def add_news_card_to_file(file_path, title, date, image_src, news_link, secondary_link):
    try:
        with open(resource_path(file_path), "r", encoding="utf-8") as file:
            content = file.read()

        marker = "<!-- يمكنك إضافة المزيد من البطاقات هنا -->"
        if marker in content:
            new_card = f"""
            <div class="news-card" herf="{news_link}" data-src="{secondary_link}" >
                <div class="card-info" dir="rtl">
                    <h3 class="card-title">{title}</h3>
                    <img src="{image_src}" alt="صورة الخبر" class="card-icon">
                    <p class="card-date">{date}</p>
                </div>
            </div>\n            {marker}"""

            updated_content = content.replace(marker, new_card)

            with open(resource_path(file_path), "w", encoding="utf-8") as file:
                file.write(updated_content)

            return f"تمت إضافة الخبر إلى {file_path} بنجاح."
        else:
            return f"التعليق المطلوب غير موجود في {file_path}."
    except Exception as e:
        return f"حدث خطأ أثناء معالجة الملف: {e}"

def remove_last_news_card(file_path):
    try:
        with open(resource_path(file_path), "r", encoding="utf-8") as file:
            content = file.read()

        marker = "<!-- يمكنك إضافة المزيد من البطاقات هنا -->"
        if marker not in content:
            return f"التعليق '{marker}' غير موجود في {file_path}."
        
        before_marker, after_marker = content.split(marker, 1)

        last_card_start = before_marker.rfind('<div class="news-card"')
        if last_card_start == -1:
            return "لا توجد بطاقات أخبار لحذفها."

        before_marker = before_marker[:last_card_start].strip()

        updated_content = f"{before_marker}\n{marker}{after_marker}"

        with open(resource_path(file_path), "w", encoding="utf-8") as file:
            file.write(updated_content)

        return f"تم حذف آخر خبر من {file_path} بنجاح."
    
    except Exception as e:
        return f"حدث خطأ أثناء معالجة الملف: {e}"

def choose_image_folder(image_var, image_label, folder_var):
    folder_window = Toplevel()
    folder_window.title("اختر مجلد الصور")
    folder_window.geometry("400x300")

    image_list = Listbox(folder_window)
    image_list.pack(pady=10, fill='both', expand=True)

    def load_images_from_folder(folder_name):
        image_list.delete(0, 'end')

        # هنا يتم تعديل مسار الصورة ليكون مباشرة في مجلد images
        images_path = os.path.join('images', folder_name)

        if os.path.exists(images_path):
            for img in os.listdir(images_path):
                if img.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_list.insert('end', img)

    sections = [sec for sec in os.listdir(resource_path('images')) if os.path.isdir(resource_path(os.path.join('images', sec)))]

    section_var = StringVar(value="اختر قسم")
    
    section_menu = OptionMenu(folder_window, section_var, *sections, command=lambda selected: (load_images_from_folder(selected), folder_var.set(selected)))
    section_menu.pack(pady=10)

    def select_image():
        selected_image = image_list.get(image_list.curselection())
        image_var.set(selected_image)
        image_label.config(text=f"{selected_image}")
        folder_window.destroy()

    select_button = Button(folder_window, text="اختر الصورة", command=select_image, width=20, height=3)
    select_button.pack(pady=10)

def create_gui():
    root = Tk()
    root.title("نشر الاخبار")
    root.geometry("600x400")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 600
    window_height = 400
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    canvas = Canvas(root)
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    font_size = 16
    label_font = tkFont.Font(family="Cairo", size=font_size)

    title_var = StringVar()
    date_var = StringVar()
    image_var = StringVar()
    news_link_var = StringVar()
    secondary_link_var = StringVar()
    file_var = StringVar()
    folder_var = StringVar()

    Label(scrollable_frame, text="عنوان الخبر", font=label_font).pack(pady=5)
    title_entry = Entry(scrollable_frame, textvariable=title_var, font=label_font, width=50)
    title_entry.pack(pady=5)

    Label(scrollable_frame, text="تاريخ الخبر", font=label_font).pack(pady=5)
    date_entry = Entry(scrollable_frame, textvariable=date_var, font=label_font, width=50)
    date_entry.pack(pady=5)

    Label(scrollable_frame, text="اختر صورة الخبر", font=label_font).pack(pady=5)

    image_button = Button(scrollable_frame, text="اختر صورة", command=lambda: choose_image_folder(image_var, image_label, folder_var), width=20, height=3)
    image_button.pack(pady=5)

    image_label = Label(scrollable_frame, text="", font=label_font)
    image_label.pack(pady=5)

    Label(scrollable_frame, text="رابط المقال فيديوا", font=label_font).pack(pady=5)
    news_link_entry = Entry(scrollable_frame, textvariable=news_link_var, font=label_font, width=50)
    news_link_entry.pack(pady=5)

    Label(scrollable_frame, text="رابط المقال مكتوب", font=label_font).pack(pady=5)
    secondary_link_entry = Entry(scrollable_frame, textvariable=secondary_link_var, font=label_font, width=50)
    secondary_link_entry.pack(pady=5)

    note_label = Label(scrollable_frame, text=".ملاحظة : اختر إما مقال فيديو أو مقال مكتوب، لا تختار كلاهما", font=label_font , fg="red")
    note_label.pack(pady=5)

    files = {
        "news-art-culture.html": "أخبار الفن والثقافة",
        "news-community.html": "أخبار المجتمع",
        "news-economy.html": "أخبار الاقتصاد",
        "news-algeria.html": "أخبار الجزائر",
        "news-sport.html": "أخبار الرياضة",
        "news-technology.html": "أخبار التكنولوجيا",
        "news-world.html": "أخبار العالم",
    }

    Label(scrollable_frame, text="اختر القسم الذي تريد وضع الخبر فيه", font=label_font).pack(pady=5)
    file_var.set("اختر القسم")
    
    file_menu = OptionMenu(scrollable_frame, file_var, *files.values())
    file_menu.pack(pady=5)

    result_label = Label(scrollable_frame, text="", font=label_font, fg="red")
    result_label.pack(pady=5)

    button_frame = Frame(scrollable_frame)
    button_frame.pack(pady=10)

    def hide_message():
        result_label.config(text="")

    def on_submit():
        title = title_var.get().strip()
        date = date_var.get().strip()
        selected_file = file_var.get()
        selected_folder = folder_var.get()
        selected_image = image_var.get()

        if not (title and date and selected_file != "اختر القسم" and selected_image):
            result_label.config(text="يرجى ملء جميع الحقول.")
            root.after(5000, hide_message)
            return

        image_path = os.path.join('images', selected_folder, selected_image)
        selected_file_path = next((file for file, desc in files.items() if desc == selected_file), None)

        result = add_news_card_to_file(selected_file_path, title, date, image_path, news_link_var.get(), secondary_link_var.get())
        result_label.config(text=result)
        root.after(5000, hide_message)

    add_button = Button(button_frame, text="إضافة الخبر", command=on_submit, width=20)
    add_button.pack(side="left", padx=5)

    def on_remove():
        selected_file = file_var.get()
        if selected_file == "اختر القسم":
            result_label.config(text="يرجى اختيار قسم.")
            root.after(5000, hide_message)
            return

        selected_file_path = next((file for file, desc in files.items() if desc == selected_file), None)

        result = remove_last_news_card(selected_file_path)
        result_label.config(text=result)
        root.after(5000, hide_message)

    remove_button = Button(button_frame, text="حذف آخر خبر", command=on_remove, width=20)
    remove_button.pack(side="left", padx=5)


    copyright_label = Label(scrollable_frame, text="Dev instagram: @outuo_", font=tkFont.Font(family="Cairo", size=10), fg="gray")
    copyright_label.pack(side="bottom", pady=10)

    root.mainloop()

create_gui()
#Dev instagram: @outuo_