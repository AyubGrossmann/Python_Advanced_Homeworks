from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task

@receiver(pre_save, sender=Task)
def save_previous_status(sender, instance, **kwargs):
    # Запоминаем старый статус, чтобы сравнить его после сохранения.
    if instance.pk:
        try:
            old_task = Task.objects.get(pk=instance.pk)
            instance._old_status = old_task.status
        except Task.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Task)
def notify_owner_about_status(sender, instance, created, **kwargs):
    old_status = getattr(instance, "_old_status", None)

    # При создании задачи или сохранении без смены статуса письмо не нужно.
    if created or old_status is None or old_status == instance.status:
        return

    if instance.owner and instance.owner.email:
        send_mail(
            subject=f"Изменился статус задачи: {instance.title}",
            message=(
                f"Статус вашей задачи «{instance.title}» изменился "
                f"с «{old_status}» на «{instance.status}»."
            ),
            from_email=None,
            recipient_list=[instance.owner.email],
            fail_silently=False,
        )
