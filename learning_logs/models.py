from django.db import models

class Topic(models.Model):
	"""Тема, яку використовує користувач."""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		"""Повернути рядкове представлення моделі."""
		return self.text