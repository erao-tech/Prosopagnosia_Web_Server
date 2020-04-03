# import boto3
# s3 = boto3.resource('s3')
# my_bucket = s3.Bucket('ece516-bucket')
# all_reference_faces = []
# for file in my_bucket.objects.filter(Prefix="reference_faces/"):
#     if (file.key != "reference_faces/"):
#         all_reference_faces.append(file.key)
# # return all_reference_faces
a = 'reference_faces/DonaldTrump.jpg'
print(a[16:-4])