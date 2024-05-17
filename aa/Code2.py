import random
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def generate_shares(image_path, k, n):
    try:
        img = Image.open(image_path).convert('1')  # Mở hình ảnh và chuyển đổi sang ảnh nhị phân (đen trắng)
    except IOError:
        messagebox.showerror("Error", "Cannot open image file.") 
        return

    width, height = img.size  # Kích thước của hình ảnh
    shares = [Image.new('1', (width, height)) for _ in range(n)]  # Tạo danh sách shares từ hình ảnh

    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))  # Lấy giá trị pixel từ hình ảnh gốc
            bits = [random.randint(0, 1) for _ in range(n)]  # Tạo các bit ngẫu nhiên cho các share
            bits_sum = sum(bits[:k-1]) % 2  # Tính tổng các bit đầu tiên
            bits[k-1] = (pixel - bits_sum) % 2  # Tính bit thứ k dựa trên giá trị pixel và tổng các bit đầu tiên
            random.shuffle(bits)  # Trộn các bit
            for i in range(n):
                shares[i].putpixel((x, y), bits[i])  # Gán giá trị pixel cho từng share

    for i, share in enumerate(shares):
        share.save(f'share{i + 1}.png')  # Lưu các share vào các tệp PNG

    messagebox.showinfo("Success", f"{n} shares generated with {k} keys and saved in the current directory.")

def recover_image(share_paths):
    shares = []
    for share_path in share_paths:
        try:
            share = Image.open(share_path).convert('1')  # Mở mỗi share và chuyển đổi sang ảnh nhị phân
            shares.append(share)
        except IOError:
            messagebox.showerror("Error", f"Cannot open share file: {share_path}.") 
            return

    width, height = shares[0].size  # Lấy kích thước của share đầu tiên
    recovered_image = Image.new('1', (width, height))  # Tạo một hình ảnh mới để khôi phục

    for x in range(width):
        for y in range(height):
            original_pixel = sum(share.getpixel((x, y)) for share in shares) % 2  # XOR các giá trị pixel từ các share để khôi phục hình ảnh gốc
            recovered_image.putpixel((x, y), original_pixel)  # Gán giá trị pixel cho hình ảnh khôi phục

    recovered_image.save('recovered_image.png')  # File khôi phục định dạng PNG
    messagebox.showinfo("Success", "Image recovered and saved as 'recovered_image.png'.")

class VisualCryptographyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visual Cryptography (k, n)")
        self.geometry("500x500")  # Thiết lập kích thước application

        self.k_label = tk.Label(self, text="Minimum shares (k):")
        self.k_label.pack()  # Hiển thị nhãn k
        self.k_entry = tk.Entry(self)
        self.k_entry.pack()  # Hiển thị ô nhập k

        self.n_label = tk.Label(self, text="Total shares (n):")
        self.n_label.pack()
        self.n_entry = tk.Entry(self)
        self.n_entry.pack() 

        self.upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()  # Nút tải lên hình ảnh

        self.generate_button = tk.Button(self, text="Generate Shares", command=self.generate_shares)
        self.generate_button.pack()  # Nút tạo shares

        self.recover_button = tk.Button(self, text="Recover Image", command=self.recover_image)
        self.recover_button.pack()  # Nút khôi phục hình ảnh

        self.image_path = None
        self.share_paths = []

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if self.image_path:
            messagebox.showinfo("Image Uploaded", f"Image uploaded: {self.image_path}") 

    def generate_shares(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.") 
            return

        try:
            k = int(self.k_entry.get())
            n = int(self.n_entry.get())

            if k < 2 or n < 2 or k > n: # Nếu k hoặc n nhỏ hơn 2
                messagebox.showwarning("Invalid Input", "k and n must be greater than 1")  
                return

            generate_shares(self.image_path, k, n)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid integers for k and n.") 

    def recover_image(self):
        self.share_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png")])
        if not self.share_paths:
            messagebox.showwarning("No Shares", "Please select at least one share file.")
            return

        recover_image(self.share_paths)

if __name__ == '__main__':
    app = VisualCryptographyApp()
    app.mainloop()