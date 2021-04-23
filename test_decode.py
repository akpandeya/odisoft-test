import unittest

from decode import hex_to_dec, get_bool, hex_to_binary_int_string, hex_to_binary_string_list, invert_string, get_data_status
from decode import format_hex, bin_to_dec, binary_to_on_off, get_digital_io_status, get_alarm, get_reverse
from decode import get_battery, hex_to_float, make_decimal
class TestStringMethods(unittest.TestCase):

    def test_hex_to_dec(self):
        self.assertEqual(hex_to_dec('a'), '10')
        self.assertEqual(hex_to_dec('fe', '28'), '214')
        with self.assertRaises(AssertionError):
            hex_to_dec('cat')
    def test_bin_to_dec(self):
        self.assertEqual(bin_to_dec('00'), '0')
        self.assertEqual(bin_to_dec('01'), '1')
        self.assertEqual(bin_to_dec('10'), '2')
        self.assertEqual(bin_to_dec('11'), '3')
        
        with self.assertRaises(AssertionError):
            hex_to_dec('cat')
            
    def test_get_bool(self):
        self.assertEqual(get_bool('0'), 'false')
        self.assertEqual(get_bool('1'), 'true')
        self.assertEqual(get_bool('false'), 'false')
        self.assertEqual(get_bool('true'), 'true')
        self.assertEqual(get_bool('off'), 'false')
        self.assertEqual(get_bool('on'), 'true')
        with self.assertRaises(AssertionError):
            get_bool('cat')
    
    def test_binary_to_on_off(self):
        self.assertEqual(binary_to_on_off('0'), 'off')
        self.assertEqual(binary_to_on_off('1'), 'on')
        self.assertEqual(binary_to_on_off('true'), 'on')
        self.assertEqual(binary_to_on_off('false'), 'off')
        self.assertEqual(binary_to_on_off('on'), 'on')
        self.assertEqual(binary_to_on_off('off'), 'off')
        with self.assertRaises(AssertionError):
            binary_to_on_off('cat')

    def test_hex_to_binary_int_string(self):
        self.assertEqual(hex_to_binary_int_string('0', 2), '00')
        self.assertEqual(hex_to_binary_int_string('1', 2), '01')
        self.assertEqual(hex_to_binary_int_string('1', 3), '001')
        self.assertEqual(hex_to_binary_int_string('7', 4), '0111')
        self.assertEqual(hex_to_binary_int_string("a134", 16), '1010000100110100')

    def test_hex_to_binary_string_list(self):
        self.assertEqual(hex_to_binary_string_list('1', 4), ['false', 'false', 'false', 'true'])
        self.assertEqual(hex_to_binary_string_list('0', 4), ['false', 'false', 'false', 'false'])
        self.assertEqual(hex_to_binary_string_list('2', 4), ['false', 'false', 'true', 'false'])
        self.assertEqual(hex_to_binary_string_list('4', 4), ['false', 'true', 'false', 'false'])
        self.assertEqual(hex_to_binary_string_list('8', 4), ['true', 'false', 'false', 'false'])
        self.assertEqual(hex_to_binary_string_list('4', 4, 3), ['false', 'true', 'false'])
        self.assertEqual(hex_to_binary_string_list("a134", 16), ['true', 'false', 'true', 'false', 'false', 'false', 'false','true', 'false','false', 'true', 'true', 'false','true', 'false', 'false'])

    def test_get_digital_io_status(self):
        self.assertEqual(get_digital_io_status('0000'), ['true', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('1000'), ['true', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('2000'), ['true', 'false', 'true', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('4000'), ['true', 'true', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8000'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8100'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8200'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8400'), ['false', 'false', 'false', 'false', 'false', 'false', 'true'])
        self.assertEqual(get_digital_io_status('8800'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8810'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8820'), ['false', 'false', 'false', 'false', 'true', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8840'), ['false', 'false', 'false', 'true', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8880'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8881'), ['false', 'false', 'false', 'false', 'false', 'true', 'false'])
        self.assertEqual(get_digital_io_status('8882'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8884'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        self.assertEqual(get_digital_io_status('8888'), ['false', 'false', 'false', 'false', 'false', 'false', 'false'])
        
    def test_get_alarm(self):
        self.assertEqual(get_alarm("00"), ['0','']) #0
        self.assertEqual(get_alarm("09"), ['0','']) #0
        self.assertEqual(get_alarm("0a"), ['0','']) #0
        self.assertEqual(get_alarm("0f"), ['0','']) #0
        
        self.assertEqual(get_alarm("10"), ['10','Anti_theft Alarm']) #10
        self.assertEqual(get_alarm("11"), ['11','Analog 1 voltage increase']) #11
        self.assertEqual(get_alarm("12"), ['12','Analog 1 voltage decrease']) #12
        self.assertEqual(get_alarm("13"), ['13','Analog 2 voltage increase']) #13
        self.assertEqual(get_alarm("14"), ['14','Analog 2 voltage decrease']) #14
        self.assertEqual(get_alarm("15"), ['15','ACC on']) #15
        self.assertEqual(get_alarm("16"), ['16','ACC off']) #16
        self.assertEqual(get_alarm("17"), ['17','AC on']) #17
        self.assertEqual(get_alarm("18"), ['18','AC off']) #18
        self.assertEqual(get_alarm("19"), ['19','Idle start']) #19
        self.assertEqual(get_alarm("1a"), ['1','External power disconnect']) #1
        self.assertEqual(get_alarm("1b"), ['1','External power disconnect']) #1
        self.assertEqual(get_alarm("1c"), ['1','External power disconnect']) #1
        self.assertEqual(get_alarm("1d"), ['1','External power disconnect']) #1
        self.assertEqual(get_alarm("1e"), ['1','External power disconnect']) #1
        self.assertEqual(get_alarm("1f"), ['1','External power disconnect']) #1
        
        
        self.assertEqual(get_alarm("20"), ['20','Idle end'])#20 
        self.assertEqual(get_alarm("21"), ['21','GSM jammer detection start'])
        self.assertEqual(get_alarm("22"), ['22','GSM jammer detection end'])
        self.assertEqual(get_alarm("23"), ['23','External power recover'])
        self.assertEqual(get_alarm("24"), ['24','External power lower'])
        self.assertEqual(get_alarm("25"), ['25','digital 3 input from 0 to 1'])
        self.assertEqual(get_alarm("26"), ['26','digital 3 input from 1 to 0'])
        self.assertEqual(get_alarm("27"), ['27','digital 4 input from 0 to 1'])
        self.assertEqual(get_alarm("28"), ['28','digital 4 input from 1 to 0'])
        self.assertEqual(get_alarm("29"), ['29','digital 5 input from 1 to 0'])
        self.assertEqual(get_alarm("2a"), ['2','Inner power lower'])
        self.assertEqual(get_alarm("2b"), ['2','Inner power lower'])
        self.assertEqual(get_alarm("2c"), ['2','Inner power lower'])
        self.assertEqual(get_alarm("2d"), ['2','Inner power lower'])
        self.assertEqual(get_alarm("2e"), ['2','Inner power lower'])
        self.assertEqual(get_alarm("2f"), ['2','Inner power lower'])
        
        self.assertEqual(get_alarm("30"), ['30','digital 5 input from 0 to 1'])#30 
        self.assertEqual(get_alarm("31"), ['31','digital 6 input from 1 to 0'])
        self.assertEqual(get_alarm("32"), ['32','digital 6 input from 0 to 1'])
        self.assertEqual(get_alarm("33"), ['33','Analog 3 voltage increase'])
        self.assertEqual(get_alarm("34"), ['34','Analog 3 voltage decrease'])
        self.assertEqual(get_alarm("35"), ['35','Analog 4 voltage increase'])
        self.assertEqual(get_alarm("36"), ['36','Analog 4 voltage decrease'])
        self.assertEqual(get_alarm("37"), ['37','Analog 4 voltage decrease'])
        self.assertEqual(get_alarm("38"), ['38',''])
        self.assertEqual(get_alarm("39"), ['39',''])
        self.assertEqual(get_alarm("3a"), ['3','SOS'])
        self.assertEqual(get_alarm("3b"), ['3','SOS'])
        self.assertEqual(get_alarm("3c"), ['3','SOS'])
        self.assertEqual(get_alarm("3d"), ['3','SOS'])
        self.assertEqual(get_alarm("3e"), ['3','SOS'])
        self.assertEqual(get_alarm("3f"), ['3','SOS'])
        
        self.assertEqual(get_alarm("40"), ['40',''])
        self.assertEqual(get_alarm("41"), ['41',''])
        self.assertEqual(get_alarm("42"), ['42',''])
        self.assertEqual(get_alarm("43"), ['43',''])
        self.assertEqual(get_alarm("44"), ['44',''])
        self.assertEqual(get_alarm("45"), ['45',''])
        self.assertEqual(get_alarm("46"), ['46',''])
        self.assertEqual(get_alarm("47"), ['47',''])
        self.assertEqual(get_alarm("48"), ['48',''])
        self.assertEqual(get_alarm("49"), ['49','']) 
        self.assertEqual(get_alarm("4a"), ['4','Over speed'])
        self.assertEqual(get_alarm("4b"), ['4','Over speed'])
        self.assertEqual(get_alarm("4c"), ['4','Over speed'])
        self.assertEqual(get_alarm("4d"), ['4','Over speed'])
        self.assertEqual(get_alarm("4e"), ['4','Over speed'])
        self.assertEqual(get_alarm("4f"), ['4','Over speed'])
        
        
        self.assertEqual(get_alarm("50"), ['50',''])
        self.assertEqual(get_alarm("59"), ['59',''])
        self.assertEqual(get_alarm("5a"), ['5','In geofence'])
        self.assertEqual(get_alarm("5f"), ['5','In geofence'])
        
        self.assertEqual(get_alarm("60"), ['60',''])
        self.assertEqual(get_alarm("69"), ['69',''])
        self.assertEqual(get_alarm("6a"), ['6','out geofence'])
        self.assertEqual(get_alarm("6f"), ['6','out geofence'])
        
        self.assertEqual(get_alarm("70"), ['70',''])
        self.assertEqual(get_alarm("79"), ['79',''])
        self.assertEqual(get_alarm("7a"), ['7','Drag alarm'])
        self.assertEqual(get_alarm("7f"), ['7','Drag alarm'])
        
        self.assertEqual(get_alarm("80"), ['80',''])
        self.assertEqual(get_alarm("89"), ['89',''])
        self.assertEqual(get_alarm("8a"), ['8','Vibration alarm'])
        self.assertEqual(get_alarm("8f"), ['8','Vibration alarm'])
        
        self.assertEqual(get_alarm("90"), ['90', ''])
        self.assertEqual(get_alarm("99"), ['99', '']) 
        self.assertEqual(get_alarm("9a"), ['9', 'Device apply address'])
        self.assertEqual(get_alarm("9f"), ['9', 'Device apply address'])
        
        self.assertEqual(get_alarm("a0"), ['NaN', ''])
        self.assertEqual(get_alarm("a9"), ['NaN', ''])
        self.assertEqual(get_alarm("aa"), ['NaN', ''])
        self.assertEqual(get_alarm("af"), ['NaN', ''])
        self.assertEqual(get_alarm("ff"), ['NaN', ''])
        with self.assertRaises(AssertionError):
            get_alarm('1t')
        with self.assertRaises(AssertionError):
            get_alarm('1')
        with self.assertRaises(AssertionError):
            get_alarm('134')

    def test_invert_string(self):
        self.assertEqual(invert_string('true'), 'false')
        self.assertEqual(invert_string('false'), 'true')
        with self.assertRaises(AssertionError):
            invert_string('0')
    def test_get_data_status(self):
        self.assertEqual(get_data_status('4'), ['false', 'true', 'true'])
          
          
    def test_format_hex(self):
        self.assertEqual(format_hex("1234"), "[12 34]")
        self.assertEqual(format_hex("12345678"), "[12 34 56 78]")  
    
    def test_get_reverse(self):
        self.assertEqual(get_reverse('00'), ["GPS+Glonass satellite system", "false", "false"]) #GPS+Glonass satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('10'), ["GPS+Glonass satellite system", "false", "false"]) #GPS+Glonass satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('20'), ["GPS+Glonass satellite system", "false", "false"]) #GPS+Glonass satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('30'), ["GPS+Glonass satellite system", "false", "false"]) #GPS+Glonass satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('40'), ["GPS+Galileo satellite system", "false", "false"]) #GPS state: SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('50'), ["GPS+Galileo satellite system", "false", "false"]) #GPS state:GPS+Galileo satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('60'), ["GPS+Galileo satellite system", "false", "false"]) #GPS state:GPS+Galileo satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('70'), ["GPS+Galileo satellite system", "false", "false"]) #GPS state:GPS+Galileo satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('80'), ["GPS+Beidou satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('90'), ["GPS+Beidou satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('a0'), ["GPS+Beidou satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('b0'), ["GPS+Beidou satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('c0'), ["GPS+Galileo satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('d0'), ["GPS+Galileo satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('e0'), ["GPS+Galileo satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('f0'), ["GPS+Galileo satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('88'), ["GPS+Beidou satellite system", "false", "false"]) #GPS state: SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('af'), ["GPS+Beidou satellite system", "false", "false"]) #GPS state:GPS+Beidou satellite system SMS alarm open:false:Digtal 2 alarm open:false
        self.assertEqual(get_reverse('ff'), ["GPS+Galileo satellite system", "false", "false"])#GPS state:GPS+Galileo satellite system SMS alarm open:false:Digtal 2 alarm open:false

    def test_get_battery(self):
        self.assertEqual(get_battery('00'), '100')
        self.assertEqual(get_battery('01'), '1')
        self.assertEqual(get_battery('21'), '21')
        self.assertEqual(get_battery('31'), '31')
        self.assertEqual(get_battery('41'), '41')
        self.assertEqual(get_battery('51'), '51')
        self.assertEqual(get_battery('61'), '61')
        self.assertEqual(get_battery('75'), '75')
        self.assertEqual(get_battery('83'), '83')
        self.assertEqual(get_battery('99'), '99')
        self.assertEqual(get_battery('a1'), 'NaN')
        self.assertEqual(get_battery('ab'), 'NaN')
        self.assertEqual(get_battery('c2'), 'NaN')
        self.assertEqual(get_battery('2d'), 'NaN')
        self.assertEqual(get_battery('2e'), 'NaN')
        self.assertEqual(get_battery('2f'), 'NaN')
        with self.assertRaises(AssertionError):
                get_battery('123')
        with self.assertRaises(AssertionError):
                get_battery('1t')
    
    def test_hex_to_float(self):
        self.assertEqual(hex_to_float('00000000'), '0')
        self.assertEqual(hex_to_float('00000001'), '2.350988701644575E-38')
        self.assertEqual(hex_to_float('00000002'), '9.4039548065783E-38')
        self.assertEqual(hex_to_float('00000003'), '3.76158192263132E-37')
        self.assertEqual(hex_to_float('00000004'), '1.504632769052528E-36')
        self.assertEqual(hex_to_float('00000008'), '3.851859888774472E-34')
        self.assertEqual(hex_to_float('0000000f'), '6.310887241768095E-30')
        self.assertEqual(hex_to_float('00000010'), '2.524354896707238E-29')
        self.assertEqual(hex_to_float('00000020'), '1.0842021724855044E-19')
        self.assertEqual(hex_to_float('00000040'), '2')
        self.assertEqual(hex_to_float('0000e841'), '29')
        self.assertEqual(hex_to_float('976fbfc2'), '-95.71794891357422')
        self.assertEqual(hex_to_float('c650ee41'), '29.789440155029297')
    
    def test_get_ext_supply(self):
        self.assertEqual(make_decimal('1234', 2), '12.34')
        self.assertEqual(make_decimal('123a', 2), '1.23')
        self.assertEqual(make_decimal('12aa', 2), '0.12')
        self.assertEqual(make_decimal('1aaa', 2), '0.01')
        self.assertEqual(make_decimal('aaaa', 2), 'NaN')
        self.assertEqual(make_decimal('1234', 3), '123.4')
        self.assertEqual(make_decimal('123a', 3), '12.3')
        self.assertEqual(make_decimal('12aa', 3), '1.2')
        self.assertEqual(make_decimal('1aaa', 3), '0.1')
        self.assertEqual(make_decimal('0000', 3), '0')
        
        
        
        
        
if __name__ == '__main__':
    unittest.main()