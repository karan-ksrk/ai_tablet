# import os
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
# from reportlab.platypus.flowables import Flowable
# from reportlab.lib.units import inch
# from reportlab.platypus import Spacer

# class ImageGrid(Flowable):
#     def __init__(self, images, max_images_per_row=2, image_width=2*inch, image_height=2*inch, padding=0.1*inch):
#         super().__init__()
#         self.images = images
#         self.max_images_per_row = max_images_per_row
#         self.image_width = image_width
#         self.image_height = image_height
#         self.padding = padding

#     def wrap(self, width, height):
#         self.width = width
#         self.height = height
#         return self.width, self.height

#     def draw(self):
#         max_width = self.max_images_per_row * (self.image_width + self.padding) - self.padding
#         current_x = 0
#         current_y = self.height

#         for img_path in self.images:
#             if current_x + self.image_width > max_width:
#                 current_x = 0
#                 current_y -= self.image_height + self.padding

#             self.canv.drawImage(img_path, current_x, current_y - self.image_height, width=self.image_width, height=self.image_height)
#             current_x += self.image_width + self.padding

# def create_pdf(folder_path, pdf):
#     images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

#     style = getSampleStyleSheet()
#     pdf_elements = []
#     pdf_elements.append(Paragraph(folder_path.split('/')[-1], style['Heading1']))
#     pdf_elements.append(Spacer(1, 12))
#     img_grid = ImageGrid(images)
#     pdf_elements.append(img_grid)
#     pdf_elements.append(PageBreak())

#     pdf.build(pdf_elements)

# def main():
#     root_folder = 'tags'  # Path to the root folder
#     pdf = SimpleDocTemplate("output.pdf", pagesize=A4)

#     for folder_name in os.listdir(root_folder):
#         folder_path = os.path.join(root_folder, folder_name)
#         if os.path.isdir(folder_path):
#             create_pdf(folder_path, pdf)

# if __name__ == "__main__":
#     main()


import os
from fpdf import FPDF

# Function to get list of image files in a directory
def get_image_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Function to create PDF for a folder
def create_pdf(folder_path, pdf):
    images = get_image_files(folder_path)
     # Calculate image grid dimensions
    grid_rows = 10
    grid_cols = 7
    images_per_page = grid_rows * grid_cols
    img_width = 25
    img_height = 25
    padding_x = 2
    padding_y = 2
    
    # Add pages and images
    for idx, image_path in enumerate(images):
        if idx % images_per_page == 0 and idx != 0:  # Add new page after every 'images_per_page' images, except the first one
            pdf.add_page()
        row = (idx // grid_cols) % grid_rows
        col = idx % grid_cols
        x = col * (img_width + padding_x) + 10
        y = row * (img_height + padding_y) + 20
        pdf.image(image_path, x = x, y = y, w = img_width)

# Main function to iterate over folders and create PDF
def main():
    root_folder = 'tags'  # Path to the root folder
    folder_names = ["tags_DICT_6X6_1000"]
    for folder_name in folder_names:
    # for folder_name in os.listdir(root_folder):
        pdf = FPDF()
        folder_path = os.path.join(root_folder, folder_name)
        pdf.set_font("Arial", size = 12)
        pdf.add_page()
        pdf.cell(200, 10, txt = folder_path.split('/')[-1], ln = True, align = 'C')
        pdf.ln(10)
        if os.path.isdir(folder_path):
            create_pdf(folder_path, pdf)
        pdf.output(f"all_aruco/{folder_name}.pdf")

if __name__ == "__main__":
    main()
