# ObjDet-utils-pack

## Notes before proceeding
- Sometime paths are hard-coded (sorry), so you need to change them. (update coming soon)
- update labelmap.pbtxt according to your labels
- run _setup_dataset.py_ -d dir_name


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

## Pipeline template

<pre><code>

@echo off

echo. && echo "Build training/test csv and autoscale bboxes"
build_csv.py -d F:\datasets\people\people_1 -m xml -s 300 300

echo. && echo "Resizing train pics in a separate folder.."
resize_images.py -d train/imgs_resized/ -s 300 300

echo. && echo "Resizing test pics.."
resize_images.py -d test/imgs_resized/ -s 300 300

echo. && echo "Generating tfrecords.."

generate_tfrecord.py --csv_input=test_labels.csv --output_path=test.tfrecord --image_dir=test/imgs_resized
generate_tfrecord.py --csv_input=train_labels.csv --output_path=train.tfrecord --image_dir=train/imgs_resized


pause

</code> </pre>