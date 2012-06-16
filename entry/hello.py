@csrf_exempt
def hello(request):
    try:
        t = Tropo()
        msg = request.POST['msg']

        s = Session(request.body)
        cell = s.fromaddress['id']
        print('Cell #%s' % cell)

# lookup patient with this cell #
        if cell[0] is '1':   # trim leading 1 in cell # if there
            cell = cell[1:]
        p = Patient.objects.filter(cell=cell)   # all patients with this cell #
        if p.exists():                                    # if cell # found then create new entry
            if p.count>1
                print('WARNING: Multiple patients with cell # %s' % cell)
            parent = p[0]  # assume first 
            entry = Entry(patient=parent, entry=msg)
            entry.save()
            json = t.say("Entry saved, thank you " + parent.name)
            json = t.RenderJson(json)
        else:                                               # if cell # NOT found then notify
            json = t.say("Could not find patient with cell # " + cell)
            json = t.RenderJson(json)
    
        return HttpResponse(json) 
    except Exception, err:
        print('ERROR: %s\n' % str(err))

