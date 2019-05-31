import random

class Teacher(object):
  def __init__(self, name, sex, can_teach_subject, can_attend, can_manage, shift=None):
    self.name = name
    self.sex = sex
    self.can_teach_subject = can_teach_subject
    self.can_attend = can_attend
    self.can_manage = can_manage
    if (shift == None):
      rand_shift = []
      for _ in range(18):
        rand_shift.append(random.randint(0, 1))
      self.shift = rand_shift
    else:
      self.shift = shift



class Student(object):
  def __init__(self, name, sex, age, take_subject, can_attend):
    self.name = name
    self.sex = sex
    self.age = age
    self.take_subject = take_subject
    self.can_attend = can_attend


class Shift(object):
  SHIFT_BOXES = [
    'mon_a', 'mon_b', 'mon_c'
    'tue_a', 'tue_b', 'tue_c'
    'wed_a', 'wed_b', 'wed_c'
    'thu_a', 'thu_b', 'thu_c'
    'fri_a', 'fri_b', 'fri_c'
    'sut_a', 'sut_b', 'sut_c'
  ]

teachers = []
students = []

seki_subject = ['math', 'english', 'science']
seki_can_attend = ['mon_b', 'mon_c', 'tue_b', 'tue_c', 'sut_a', 'sut_b', 'sut_c']
seki = Teacher('seki', 'male', seki_subject, seki_can_attend, True)

yamamoto_subject = ['math', 'english', 'science', 'phisics']
yamamoto_can_attend = ['mon_b', 'mon_c', 'tue_b', 'tue_c', 'wed_b', 'wed_c', 'fri_c']
yamamoto = Teacher('yamamoto', 'male', yamamoto_subject, yamamoto_can_attend, True)

oguti_take_subject = ['math', 'english']
oguti_can_attend = ['mon_b', 'mon_c', 'tue_b', 'tue_c', 'wed_b', 'wed_c']
oguti = Student('oguti', 'male', 15, oguti_take_subject, oguti_can_attend)

maesaka_take_subject = ['phsics']
maesaka_can_attend = ['mon_c',  'tue_c', 'fri_c']
maesaka = Student('maesaka', 'male', 18, maesaka_take_subject, maesaka_can_attend)

students.append(oguti)
students.append(maesaka)
teachers.append(seki)
teachers.append(yamamoto)
