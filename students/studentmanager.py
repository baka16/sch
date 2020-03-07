from django.db import models

class AdmissionQuerySet(models.query.QuerySet):
    def search(self, query):  # Admission.objects.all().search(query) #Admission.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                models.Q(first_name__icontains=query) | models.Q(first_name__iexact=query) | models.Q(
                    last_name__icontains=query) | models.Q(last_name__iexact=query) | models.Q(stid__iexact=query)
            ).distinct()
        return self


class AdmissionManager(models.Manager):
    def get_queryset(self):
        return AdmissionQuerySet(self.model, using=self._db)

    def search(self, query):  # Admission.objects.search()
        return self.get_queryset().search(query)



class PerformanceQuerySet(models.query.QuerySet):
    def search(self, query):  # Admission.objects.all().search(query) #Admission.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                models.Q(first_name__icontains=query) | models.Q(first_name__iexact=query) | models.Q(
                    last_name__icontains=query) | models.Q(last_name__iexact=query) | models.Q(stid__iexact=query)
            ).distinct()
        return self


class PerformanceManager(models.Manager):
    def get_queryset(self):
        return AdmissionQuerySet(self.model, using=self._db)

    def search(self, query):  # Admission.objects.search()
        return self.get_queryset().search(query)
