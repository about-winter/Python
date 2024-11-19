from tkinter import *
from tkinter import filedialog, messagebox
from threading import Thread
import yt_dlp
import os

#用yt_dlp库来获取视频信息
#增加了其他类型的报错提示
#由clauld提供技术支持
def threading():
    t1 = Thread(target=download)
    t1.start()


def download():
    try:
        # 获取输入的URL
        video_url = url_box.get()
        if not video_url:
            messagebox.showerror("Error", "请输入YouTube视频链接")
            return

        # 选择保存位置
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")]
        )

        if not save_path:
            messagebox.showwarning('取消', '下载已取消！')
            return

        # 更新状态
        status_label.config(text="正在获取视频信息...")
        root.update()

        # 设置下载选项
        ydl_opts = {
            'format': 'best',  # 下载最好的质量
            'outtmpl': save_path,  # 保存路径
            'progress_hooks': [progress_hook],  # 进度回调
        }

        # 开始下载
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        status_label.config(text="下载完成！")
        messagebox.showinfo('成功', '下载完成！')

    except Exception as e:
        status_label.config(text="下载失败")
        messagebox.showerror("Error", f"下载失败:\n{str(e)}")


def progress_hook(d):
    if d['status'] == 'downloading':
        # 计算下载进度百分比
        try:
            percent = d['_percent_str'].strip()
            status_label.config(text=f"正在下载... {percent}")
            root.update()
        except:
            pass
    elif d['status'] == 'finished':
        status_label.config(text="正在处理...")
        root.update()


# GUI部分
root = Tk()
root.title('YouTube Downloader')
root.geometry('780x500+200+200')
root.configure(bg='olivedrab1')
root.resizable(False, False)

introlable = Label(
    root,
    text='YouTube Video Downloader',
    width=30,
    relief='ridge',
    bd=4,
    font=('chiller', 26, 'italic bold'),
    fg='red')
introlable.place(x=35, y=20)

Label(
    root,
    text='Enter YouTube Link',
    font=('sans-serif', 16),
    bg='olivedrab1'
).place(x=40, y=150)

url_box = Entry(
    root,
    font=('arial', 30),
    width=30
)
url_box.place(x=40, y=180)

# 状态标签
status_label = Label(
    root,
    text="就绪",
    font=('sans-serif', 12),
    bg='olivedrab1'
)
status_label.place(x=40, y=300)

btn = Button(
    root,
    text='DOWNLOAD',
    font=('sans-serif', 25),
    command=threading
)
btn.place(x=270, y=240)

root.mainloop()
