from rest_framework import serializers
from .models import PotholeReport
from PIL import Image
import numpy as np
# import sys
# sys.path.append("..")
from utility.utils import process_img, tf_model, CATEGORIES


class PotholeReportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PotholeReport
        # fields = ['id', 'title', 'desc', 'road_img', 'class_label', 'geo_location', 'reported_at', 'user']
        fields = '__all__'
        read_only_fields = ['id', 'class_label', 'reported_at']

    def validate(self, attrs):
        request = self.context.get('request').data
        print(request)

        img_file = request.get('road_img')
        if img_file is None:
            return attrs
        
        pil_img = Image.open(img_file)
        preparedImage = process_img(pil_img)
        label = tf_model.predict([preparedImage])
        
        label_idx = np.argmax(label)
        class_category = CATEGORIES[label_idx]
        print(f"Image is of {class_category} road")

        if not label_idx:
            res_error =  serializers.ValidationError({"class_label" : class_category})
            res_error.status_code = 200
            print(res_error)
            raise res_error

        attrs['class_label'] = class_category
        return attrs
