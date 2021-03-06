import moviepy.editor as mpe
import numpy as np
import numpy.random
import os.path
import scipy.misc
import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

def demo1(train_data):
    
    td = train_data
    
    feature, label = td.sess.run([td.features, td.labels])
    
    feed_dict = {td.gene_minput: feature}
    gene_output = td.sess.run(td.gene_moutput, feed_dict=feed_dict)
    
    size = [label.shape[1], label.shape[2]]

    nearest = tf.image.resize_nearest_neighbor(feature, size)
    nearest = tf.maximum(tf.minimum(nearest, 1.0), 0.0)

    bicubic = tf.image.resize_bicubic(feature, size)
    bicubic = tf.maximum(tf.minimum(bicubic, 1.0), 0.0)

    clipped = tf.maximum(tf.minimum(gene_output, 1.0), 0.0)
    
    image   = tf.concat(2, [nearest, bicubic, clipped, label])

    image = image[0:max_samples,:,:,:]
    image = td.sess.run(image)
   
    #_summarize_progress(td, test_feature, test_label, gene_output, batch, 'out')
    
    filename = 'demo_output.png'
    filename = os.path.join(FLAGS.train_dir, filename)
    scipy.misc.toimage(clipped, cmin=0., cmax=1.).save(filename)
    print("    Saved %s" % (filename,))
            
            
    """Demo based on images dumped during training"""
    # Get images that were dumped during training
#     filenames = tf.gfile.ListDirectory(FLAGS.train_dir)
#     filenames = sorted(filenames)
#     filenames = [os.path.join(FLAGS.train_dir, f) for f in filenames if f[-4:]=='.png']

#     assert len(filenames) >= 1

#     fps        = 30

#     # Create video file from PNGs
#     print("Producing video file...")
#     filename  = os.path.join(FLAGS.train_dir, 'demo1.mp4')
#     clip      = mpe.ImageSequenceClip(filenames, fps=fps)
#     clip.write_videofile(filename)
#     print("Done!")
    
