#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from signup.models import SignupQueue

class CreateUserTestCase(TestCase):

  def setUp(self):
    SignupQueue.objects.create(email="a@a.com", name="John Doe", organization="ABC Inc.")

  def testSimpleCreate(self):
    req = SignupQueue.objects.get(organization="ABC Inc.")
    result = req.create_user()
    self.assertEqual(result[0], "johndoe")
    self.assertIsNotNone(result[1])

  def testCreateUserAlreadyLinked(self):
    req = SignupQueue.objects.get(organization="ABC Inc.")
    result = req.create_user()
    self.assertEqual(result[0], "johndoe")
    self.assertIsNotNone(result[1])

    # Now try again - we get the user back, not a password
    self.assertEqual(req.create_user(), ("johndoe", None))

  def testCreateUserNameAlreadyExists(self):
    req = SignupQueue.objects.get(organization="ABC Inc.")
    req.create_user()



  def testAccentedNames(self):
    req = SignupQueue.objects.get(organization="ABC Inc.")
    req.name=u"René Jansen"
    req.save()

    result = req.create_user()
    self.assertEqual(result[0], u"renejansen")
    self.assertIsNotNone(result[1])
