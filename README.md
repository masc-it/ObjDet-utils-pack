# ObjDet-utils-pack

Sometime paths are hard-coded (sorry), so you need to change them. (update soon)

## Notes for "generate_tf_record.py"

Remember to change class names accordingly to your labels (line 27) before running the script:

<pre><code>
def class_text_to_int(row_label):
    if row_label == 'mega':
        return 1
    elif row_label=='heltec':
        return 2
    elif row_label=='uva':
        return 1
    else:
        return 1
</code> </pre>
