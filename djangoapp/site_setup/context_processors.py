from site_setup.models import SiteSetup

def context_processor_example(request):
    return {
        # 'site_setup': SiteSetup.objects.first(),
        'example': 'Example Context Processor',
    }

def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()

    
    return {
        # 'site_setup': SiteSetup.objects.first(),
        'site_setup': setup,
    }