#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re

from cleaning.chn_company.match_dict import categoryName_dict, industryCategoriesName_dict


def match_cateName(cur_categoryName):
    if cur_categoryName in categoryName_dict.keys():
        categoryName = categoryName_dict[cur_categoryName]
        return categoryName
    else:
        return cur_categoryName


def match_industryCateName(cur_industryCategoriesName):
    if cur_industryCategoriesName in industryCategoriesName_dict.keys():
        industryCategoriesName = industryCategoriesName_dict[cur_industryCategoriesName]
        return industryCategoriesName
    else:
        return cur_industryCategoriesName


def pack(cur_categoryName,cur_industryCategoriesCode,cur_industryCategoriesName,securityCode,companyName):
    return [cur_categoryName,cur_industryCategoriesCode,cur_industryCategoriesName,securityCode,companyName]


def data_pack_insert(out_put_box, cur_categoryName,cur_industryCategoriesCode,cur_industryCategoriesName,
                                      securityCode,companyName):
    company_values = pack(cur_categoryName,cur_industryCategoriesCode,cur_industryCategoriesName,
                                      securityCode,companyName)
    out_put_box.append(company_values)


def special_handling(categoryName):
    categoryName = re.sub(r"\(|\)", '', categoryName)
    return categoryName