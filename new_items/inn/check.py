import numpy as np
import innvestigate, mnist
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img
from tensorflow.keras.preprocessing.image import img_to_array

tf.compat.v1.disable_eager_execution()
files = ["babbo_natale2.jpeg", "mamma_natale_2.jpeg", "babbo_natale_verde.jpeg", "jumper3.jpeg", "jumper2.jpeg", "babbo_natale.jpeg",          "bambina_natale.jpeg", "mamma_natale_3.jpeg",
         "jumper2.jpeg", "mamma_natale_2.jpeg"]

color = False
if color == False:
    model = load_model("santa_detector_short_bw")

    for f in files:
        image = load_img(f, target_size = (150, 150), color_mode='grayscale')
                   
        image = img_to_array(image)
        #image = image / 255
        image = image.reshape(150, 150, 1)
        
        analyzer = innvestigate.create_analyzer("guided_backprop", #"lrp.epsilon", #"gradient",
                                                innvestigate.model_wo_softmax(model))

        analysis = analyzer.analyze(np.array([image]))
        delta_up = analysis.max() - analysis.mean()
        delta_down = analysis.mean() - analysis.min()
        plt.imshow(analysis.squeeze(),
                   cmap="bwr",
                   interpolation="nearest",
                   vmin=analysis.mean() - min(delta_up, delta_down),
                   vmax=analysis.mean() + min(delta_up, delta_down))
        #plt.colorbar()
        plt.savefig(f.split(".")[0] + "_ana.png")
else:
    model = load_model("santa_detector_short_v2")
    for f in files:
        image = load_img(f, target_size = (150, 150))
                   
        image = img_to_array(image)
        #image = image / 255
        image = image.reshape(150, 150, 3)
                      
        analyzer = innvestigate.create_analyzer("guided_backprop", #"lrp.epsilon", #"gradient",
                                                innvestigate.model_wo_softmax(model),
                                                #**{"epsilon":1}
        )

        analysis = analyzer.analyze(np.array([image]))
        print(analysis.shape)
        delta_up = analysis.max() - analysis.mean()
        delta_down = analysis.mean() - analysis.min()
        plt.imshow(analysis.squeeze(),
                   cmap="bwr",
                   interpolation="nearest",
                   vmin=analysis.mean() - min(delta_up, delta_down),
                   vmax=analysis.mean() + min(delta_up, delta_down))
        #plt.colorbar()
        plt.savefig(f.split(".")[0] + "_ana_color.png")
