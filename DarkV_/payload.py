# -*- coding: utf-8 -*-
import os


def generate_folder_structure(base_path, blacklist=None):
    folder_structure = {}
    for foldername, subfolders, filenames in os.walk(base_path):
        relative_path = os.path.relpath(foldername, base_path)

        # Check if the folder is in the blacklist
        if blacklist and any(
            item in relative_path.split(os.path.sep) for item in blacklist
        ):
            continue

        if relative_path == ".":
            continue  # Skip the base folder itself
        files = [filename for filename in filenames if filename.endswith(".html")]
        folder_structure[relative_path] = files
    return folder_structure


def generate_html_file(folder_structure):
    def generate_folder_html(folder_name, files):
        folder_html = f"""
        <li class="folder-item">
            <span class="folder-name">{folder_name}</span>
            <ul class="file-list" style="display: none;">
        """
        for file in files:
            folder_html += f'<li class="file-item" data-file="{folder_name}/{file}">{file[0:(len(file)-5)]}</li>'

        folder_html += """
            </ul>
        </li>
        """
        # print(folder_html)
        return folder_html

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Пасты</title>
        <style>
        
            h1 {margin-left: 20px;}
            
            body {
                font: inherit;
                background-color: #222;
                color: #aaa;
            }
          
            aside {
                /* Правая колонка */
                position: fixed;
                top: 60px;
                right: 15px;
                width: 400px;
                /* Ширина правой колонки */
                float: right;
                /* Обтекание */
            }

            article {
                /* Левая колонка */
                margin-top: 20px;
                margin-right: 430px;
                /* Отступ справа */
            }
            
            .folder-item {
                padding: 10px;
                border: 1px solid #ccc;
                cursor: pointer;
            }
            
            .folder-name {
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .folder-name:hover {
                text-decoration: underline;
            }

            .file-item {
                padding: 5px;
                cursor: pointer;
            }

            .file-item:hover {
                text-decoration: underline;
            }
            
                #preview {
                max-width: 400px;
                 overflow-wrap: break-word;
            }
            
        </style>
        <script>
            function showPreview(file) {
                var xhr = new XMLHttpRequest();
                xhr.open("GET", file, true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        document.getElementById("preview").innerHTML = xhr.responseText;
                    }
                };
                xhr.send();
            }
            
            function bindClickEvents() {
                var folderItems = document.getElementsByClassName("folder-item");
                for (var i = 0; i < folderItems.length; i++) {
                    folderItems[i].addEventListener("click", function() {
                        var fileList = this.getElementsByClassName("file-list")[0];
                        fileList.style.display = (fileList.style.display === "none") ? "block" : "none";
                    });
                }
                
                var fileItems = document.getElementsByClassName("file-item");
                for (var i = 0; i < fileItems.length; i++) {
                    fileItems[i].addEventListener("click", function(e) {
                        e.stopPropagation(); // Prevent folder toggle when clicking a file
                        showPreview(this.getAttribute("data-file"));
                        navigator.clipboard.writeText("!паста "+this.textContent);
                        var tmp= this.textContent;
                        this.textContent="Скопировано в буфер обмена!"
                        setTimeout(() => {
                            this.textContent=tmp;
                          }, 1500);
                    });
                }
            }
            
            window.addEventListener("DOMContentLoaded", bindClickEvents);
        </script>
    </head>
    <body>
        <aside>
            <div id="preview"></div>
        </aside>
        <article>
        <h1>Список паст, доступных по команде !паста</h1>
        <ul class="folder-list">
    """
    for folder, files in folder_structure.items():
        html += generate_folder_html(folder, files)

    html += """
        </ul>
        </article>
    </body>
    </html>
    """
    # print(html)
    return html


# Define the base path where the Python script is located
base_path = os.getcwd() + r"\DarkV_"
print(base_path)
# Define the folders to exclude from the folder structure
blacklist = [".git", ".vscode"]  # Add the folders you want to exclude

# Generate the folder structure
folder_structure = generate_folder_structure(base_path, blacklist)

# Generate the HTML content
html_content = generate_html_file(folder_structure)

# Write the HTML content to a file
with open("DarkV_\index.html", "w", encoding="utf-8") as file:
    file.write(html_content)
