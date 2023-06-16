from .models import PatientDetail, PatientTestDetail, BillDetail


def CreateNewBill(total_amount):
    bill = BillDetail.objects.create(total_amount=total_amount)
    bill.save()
    return bill


def FetchAllPatients(patient_email_id):
    patients = PatientDetail.objects.filter(email_id=patient_email_id)
    return patients


def PatientBillDetails(patient_id):
    patient_bills = PatientTestDetail.objects.filter(
        patient=patient_id).values('bill').distinct()
    return patient_bills


def PatientRepostDetails(bill_id):
    patients_tests = PatientTestDetail.objects.select_related().filter(
        bill=bill_id)
    reports = []

    for testDetail in patients_tests:
        temp_data = {
            'bill_no': testDetail.bill.id,
            'bill_created_at': testDetail.bill.created_at,
            'test_price': testDetail.test.price,
            'test_name': testDetail.test.name,
            'test_sample_needed': testDetail.test.sample_needed
        }
        reports.append(temp_data)
    return reports


def PatientTestDetailsByBillId(bill_id):
    patients_tests = PatientTestDetail.objects.select_related().filter(bill=bill_id)
    tests = []

    for testDetail in patients_tests:
        temp_data = {
            'patient_name': testDetail.patient.first_name + ' ' + testDetail.patient.last_name,
            'patient_age': testDetail.patient.age,
            'test_price': testDetail.test.price,
            'test_name': testDetail.test.name,
            'test_sample_needed': testDetail.test.sample_needed
        }
        tests.append(temp_data)
    data = {
        'bill_no': testDetail.bill.id,
        'bill_amount': testDetail.bill.total_amount,
        'bill_created_at': testDetail.bill.created_at,
        'lab_name': testDetail.lab.name,
        'tests': tests
    }
    return data
