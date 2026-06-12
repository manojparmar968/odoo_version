from odoo import api, fields, models, _
from lxml import etree

class SaleOrder(models.Model):
    _inherit =  "sale.order"

    # get_view()
    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        print(self, view_id, view_type, options)
        rtn = super(SaleOrder, self).get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == "Form" and "arch" in rtn:
            doc = etree.fromstring(rtn["arch"]) 
            # fields adding method 
            add_field = etree.Element("field", {"name": "your_field_id"})
            targetd_field = doc.xpath("//field[@name='name']")
            if targetd_field:
                targetd_field[0].addnext(add_field)
            # attributes adding method
            targetd_field = doc.xpath("//field[@name='name']")
            if targetd_field:
                targetd_field[0].set("string", "field level change name!")

            rtn['arch'] = etree.tostring(doc, encoding="unicode")
        return rtn

    # name_create method
    def name_create(self, name):
        return super(SaleOrder, self).name_create(name)
            # OR 
        rtn = self.create({"name":name})
        return rtn.id, rtn.display_name
    
    def custom_method(self):
        print("clicked!!!")

        # log
        _logger.info("This is a custom log")
        _logger.debug("This is a custom log")
        _logger.error("This is a custom log")
        _logger.critical("This is a custom log")
        _logger.warning("This is a custom log")

        # search_fetch(domain, fields_list, offset, limit, order)
        self.search_fetch([], [])

        # fields_get()
        s = self.env[""]
        print(s.fields_get(allfields=["id","name"], attributes=["name", "string"]))

        # grouped
        print(self.search([]).grouped(key="order_id"))

        # _name_search(self, name, domain=None, operator='ilike', limit=None, order=None)
        def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
            return self._search(domain, limit=limit, order=order)

        # search_read()
        # search_read(domain,
        #             fields [id, name]
        #             offset=,
        #             limit=,
        #             order="",
        #             load=None)
        
        #  read_group() for pegenation
        # self.read_group(domain,
        #                 fields,
        #                 group by,
        #                 offset=
        #                 limit=
        #                 order by= ""
        #                 lazy = True
        # )
        _group_by = self.read_group([],
                                    ["id","name"],
                                    ["id","name"],lazy=False)
         
        #  read
        abc = self.search([])
        print(abc.read(fields=["name","id"], load=None))
        
        # search_count
        total_rec = self.search_count([])
    
    def copy(self, default=None):
        rtn = super(SaleOrder, self).copy(default=default)
        print(rtn)
        return rtn