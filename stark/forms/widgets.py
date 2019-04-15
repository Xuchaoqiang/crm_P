#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving

from django import forms


class DateTimePickerInput(forms.TextInput):
    template_name = 'stark/forms/widgets/datetime_picker.html'
