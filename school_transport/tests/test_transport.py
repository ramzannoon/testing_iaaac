# See LICENSE file for full copyright and licensing details.

from odoo.tests import common
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TestTransport(common.TransactionCase):

    def setUp(self):
        super(TestTransport, self).setUp()
        self.transport_vehicle_obj = self.env['fleet.vehicle']
        self.transport_driver_obj = self.env['hr.employee']
        self.transport_point_obj = self.env['transport.point']
        self.student_transport_obj = self.env['student.transport']
        self.transport_registration_obj = self.env['transport.registration']
        self.transport_participant_obj = self.env['transport.participant']
        self.transfer_vehicle_obj = self.env['transfer.vehicle']
        # self.school = self.env.ref('school.demo_school_1')
        self.contect_person = self.env.ref('hr.employee_al')
        # self.student = self.env.ref('school.demo_student_student_5')
        self.new_vehicle = self.env.ref('school_transport.transport_vehicle_1')
        currdt = datetime.now()
        tr_start_dt = datetime.strftime(currdt, DEFAULT_SERVER_DATE_FORMAT)
        tr_end_dt = currdt + rd(years=+1)
        tr_end_date = datetime.strftime(tr_end_dt, DEFAULT_SERVER_DATE_FORMAT)
        new_dt = currdt + rd(days=+2)
        rg_start_date = datetime.strftime(new_dt, DEFAULT_SERVER_DATE_FORMAT)
        rg_end_dt = new_dt + rd(months=+2)
        rg_end_date = datetime.strftime(rg_end_dt, DEFAULT_SERVER_DATE_FORMAT)
#       Create Driver
        self.driver = self.transport_driver_obj.\
            create({'name': 'Driver test',
                    'licence_no': '0554545454',
                    # 'school': self.school.id,
                    'is_driver': True
                    })
#        Create Transport Vehicle.
        print(1111111111111111111111111)
        self.transport_vehicle = self.transport_vehicle_obj.\
            create({'driver_id': self.driver.id,
                    'vehicle': 'GJ-2 6233',
                    'capacity': 56
                    })

        print(22222222222222222, self.transport_vehicle)

#        Create Transport Point.
        self.transport_point = self.transport_point_obj.\
            create({'name': 'test point-1',
                    'amount': '1000'
                    })
        self.transport_point._search([])
#        Create The Transport Root
        self.transport_root = self.student_transport_obj.\
            create({'name': 'Transport-root-1',
                    'contact_per_id': self.contect_person.id,
                    'start_date': tr_start_dt,
                    'end_date': tr_end_date,
                    'trans_vehicle_ids': [(4, self.transport_vehicle.id)],
                    'trans_point_ids': [(4, self.transport_point.id)]
                    })
        self.transport_root.transport_open()
        self.transport_root.transport_close()
        self.transport_root.participant_expire()

#        Do One Registration of The Participant
        self.transport_registration = self.transport_registration_obj.\
            create({'part_name': self.student.id,
                    'name': self.transport_root.id,
                    'vehicle_id': self.transport_vehicle.id,
                    'point_id': self.transport_point.id,
                    'for_month': 2
                    })
        self.transport_registration.onchange_point_id()
        self.transport_registration.onchange_for_month()
        self.transport_registration.trans_regi_confirm()
        self.transport_registration.trans_regi_cancel()
#        Do one entry of the transport.participant
        self.transport_participant = self.transport_participant_obj.\
            create({'name': self.student.id,
                    'transport_id': self.transport_root.id,
                    'stu_pid_id': self.student.pid,
                    'tr_reg_date': rg_start_date,
                    'tr_end_date': rg_end_date,
                    'months': 2,
                    'vehicle_id': self.transport_vehicle.id,
                    'point_id': self.transport_point.id,
                    'amount': 2000
                    })
        self.transport_participant._search([])
        self.transport_participant.set_over()
#        Do create vehicle transfer
        self.transfer_vehicle = self.transfer_vehicle_obj.\
            create({'name': self.student.id,
                    'participation_id': self.transport_participant.id,
                    'root_id': self.transport_root.id,
                    'old_vehicle_id': self.transport_vehicle.id,
                    'new_vehicle_id': self.new_vehicle.id
                    })
        self.transfer_vehicle.onchange_participation_id()
        self.transfer_vehicle.vehicle_transfer()

    def test_transport(self):
        self.assertEqual(self.student.state, 'done')
        self.assertIn(self.transport_root.trans_vehicle_ids,
                      self.transport_vehicle)
        self.assertIn(self.transport_root.trans_point_ids,
                      self.transport_point)
