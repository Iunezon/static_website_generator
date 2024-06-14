text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
splits = [i+1 for i in range(len(text) - 1) if text[i:i+2] in " *"] + [i+2 for i in range(len(text) - 1) if text[i:i+2] in "* "]
print(text[25:34])