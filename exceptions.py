class HttpError(Exception):
    """Bad Request"""
    error_code = "Bad Request"
    status_code = 400


class DatabaseError(HttpError):
    error_code = "Database Error"
    status_code = 500


[
	{
		"cost": 500.0,
		"description": "Salon treatments are designed to moisturise the hair from the inside out, restore and protect your scalp and boost hair growth. Read on to explore the variety of treatments and find the perfect one for your hair type.",
		"duration": 1,
		"id": 5,
		"style": "Treatment",
		"user_id": 1
	},
	{
		"cost": 500.0,
		"description": "A pedicure is a comprehensive treatment of your feet and is suitable for both men and women. It involves cutting, trimming and shaping your toenails, tending to your cuticles, exfoliating, hydrating and massaging your feet, and, if desired, painting your toenails",
		"duration": 1,
		"id": 6,
		"style": "pedicure",
		"user_id": 1
	},
	{
		"cost": 1500.0,
		"description": "A manicure is a beauty treatment of the hands. Your nails will be cut, filed, and shaped. You will then have your cuticles pushed back and tidied, and then enjoy a hand massage. The final step will be the painting of the nails with a colour of your choice.",
		"duration": 2,
		"id": 7,
		"style": "manicure",
		"user_id": 1
	},
	{
		"cost": 1500.0,
		"description": "Extensions can quickly and easily add volume and length, naturally enhancing your hairstyle for a different look. They can be a quick, gratifying way to compensate for a bad haircut or prepare for a special occasion.",
		"duration": 2,
		"id": 8,
		"style": "Extension Services",
		"user_id": 1
	},
	{
		"cost": 500.0,
		"description": "Hair Stylist responsibilities include cutting hair using basic and advanced techniques, consulting customers about styles and colors and applying hair care products, like treatment oils and masks. If you have experience cutting short and long hair and are up-to-date with styling trends, we'd like to meet you.",
		"duration": 1,
		"id": 9,
		"style": "Hair style",
		"user_id": 1
	}
]

[
	{
		"created": "2023-06-06T12:17:24.504453",
		"email": "eliaskarui@gmail.com",
		"firstName": "elias",
		"id": 1,
		"lastName": "kairu",
		"location": "waiyakiway road",
		"password": "$1$Y7PnlUx8$gcB8vXuq0O4.gH5QjUwjw/",
		"phoneNumber": 712345678,
		"user_role": "super_admin"
	},
	{
		"created": "2023-06-09T14:47:20.945224",
		"email": "wanjiru@gmail.com",
		"firstName": "wanjiru",
		"id": 2,
		"lastName": "Daniel",
		"location": "kiambu road",
		"password": "$1$eIymH/zl$RS45WwF64dLgQdvIdAA8K/",
		"phoneNumber": 712345678,
		"user_role": "user"
	},
	{
		"created": "2023-06-09T14:47:20.945224",
		"email": "dianakirui@gmail.com",
		"firstName": "evelyne",
		"id": 3,
		"lastName": "wanjiku",
		"location": "ruaka limuru road",
		"password": "$1$KRJ7YaOx$puQjSIU2BsCnBldRNMsBd.",
		"phoneNumber": 712345678,
		"user_role": "user"
	},
	{
		"created": "2023-06-09T14:47:20.945224",
		"email": "evelynewanjiku@gmail.com",
		"firstName": "evelyne",
		"id": 4,
		"lastName": "wanjiku",
		"location": "ruaka limuru road",
		"password": "$1$2AFhnMtr$ZHbfI/pagf42vE24cQuKJ0",
		"phoneNumber": 712345678,
		"user_role": "user"
	},
	{
		"created": "2023-06-09T14:47:20.945224",
		"email": "petermukiri@gmail.com",
		"firstName": "peter",
		"id": 5,
		"lastName": "mukiri",
		"location": "westland prarklands road",
		"password": "$1$z9A53wzO$cCtw2ORgxNERwDeTA2gL91",
		"phoneNumber": 712345678,
		"user_role": "user"
	},
	{
		"created": "2023-06-09T14:47:20.945224",
		"email": "mercymukami@gmail.com",
		"firstName": "mercy",
		"id": 6,
		"lastName": "mukami",
		"location": "westland prarklands road",
		"password": "$1$vl7BO2KA$ssPvaD1.YOj1qZvQiTSoU.",
		"phoneNumber": 712345678,
		"user_role": "user"
	}
]
