
def create_string_excryption_config(inJar, outJar, androidJar, log, output):
	configContent = '''
	<config>
    <input>
        <jar in="{0}" out="{1}"/>
    </input>
    <classpath>
        <jar name="{2}"/>
    </classpath>

	<keep-names>
		<class access="private+" stop="yes">
		<field access="private+"/>
		<method access="private+"/>
		</class>
	</keep-names>

    <property name="log-file" value="{3}"/>
    <property name="string-encryption" value="enable"/>
    <property name="string-encryption-type" value="strong"/>
    <property name="control-flow-obfuscation" value="disable"/>
    <property name="skip-renaming" value="enable"/>
    <property name="member-reorder" value="disable"/>
</config>
	'''.format(inJar, outJar, androidJar, log) 
	
	f = open(output, 'w')
	f.write(configContent)
	f.close()
	print ('configuration file can be found at '+output)

def create_control_flow_config(inJar, outJar, androidJar, log, output):
	configContent = '''
	<config>
    <input>
        <jar in="{0}" out="{1}"/>
    </input>
    <classpath>
        <jar name="{2}"/>
    </classpath>

	<keep-names>
		<class access="private+" stop="yes">
		<field access="private+"/>
		<method access="private+"/>
		</class>
	</keep-names>

    <property name="log-file" value="{3}"/>
    <property name="string-encryption" value="disable"/>
    <property name="control-flow-obfuscation" value="enable"/>
    <property name="extensive-flow-obfuscation" value="maximum"/>
    <property name="skip-renaming" value="enable"/>
    <property name="member-reorder" value="disable"/>
</config>
	'''.format(inJar, outJar, androidJar, log) 
	
	f = open(output, 'w')
	f.write(configContent)
	f.close()
	print ('configuration file can be found at '+output)


def create_reorder_member_config(inJar, outJar, androidJar, log, output):
	configContent = '''
	<config>
    <input>
        <jar in="{0}" out="{1}"/>
    </input>
    <classpath>
        <jar name="{2}"/>
    </classpath>

	<keep-names>
		<class access="private+" stop="yes">
		<field access="private+"/>
		<method access="private+"/>
		</class>
	</keep-names>

    <property name="log-file" value="{3}"/>
    <property name="string-encryption" value="disable"/>
    <property name="control-flow-obfuscation" value="disable"/>
    <property name="skip-renaming" value="enable"/>
    <property name="member-reorder" value="enable"/>
</config>
	'''.format(inJar, outJar, androidJar, log) 
	
	f = open(output, 'w')
	f.write(configContent)
	f.close()
	print ('configuration file can be found at '+output)

def create_renaming_all_config(inJar, outJar, androidJar, log, output):
	configContent = '''
	<config>
    <input>
        <jar in="{0}" out="{1}"/>
    </input>
    <classpath>
        <jar name="{2}"/>
    </classpath>

	<keep-names>
		<class access="public">
		<field access="public"/>
		<method access="public"/>
		</class>
	</keep-names>

    <property name="log-file" value="{3}"/>
    <property name="skip-renaming" value="disable"/>
    <property name="string-encryption" value="disable"/>
    <property name="control-flow-obfuscation" value="disable"/>    
    <property name="member-reorder" value="disable"/>
</config>
	'''.format(inJar, outJar, androidJar, log) 
	
	f = open(output, 'w')
	f.write(configContent)
	f.close()
	print ('configuration file can be found at '+output)

#control flow + reorder members
def create_cf_rm_config(inJar, outJar, androidJar, log, output):
	configContent = '''
	<config>
    <input>
        <jar in="{0}" out="{1}"/>
    </input>
    <classpath>
        <jar name="{2}"/>
    </classpath>

	<keep-names>
		<class access="private+" stop="yes">
		<field access="private+"/>
		<method access="private+"/>
		</class>
	</keep-names>

    <property name="log-file" value="{3}"/>
    <property name="string-encryption" value="disable"/>
    <property name="control-flow-obfuscation" value="enable"/>
    <property name="extensive-flow-obfuscation" value="maximum"/>
    <property name="skip-renaming" value="enable"/>
    <property name="member-reorder" value="enable"/>
</config>
	'''.format(inJar, outJar, androidJar, log) 
	
	f = open(output, 'w')
	f.write(configContent)
	f.close()
	print ('configuration file can be found at '+output)

#control flow + reorder members + renaming
def create_cf_rm_renaming_config(inJar, outJar, androidJar, log, output):
	configContent = '''
	<config>
    <input>
        <jar in="{0}" out="{1}"/>
    </input>
    <classpath>
        <jar name="{2}"/>
    </classpath>

	<keep-names>
		<class access="public">
		<field access="public"/>
		<method access="public"/>
		</class>
	</keep-names>

    <property name="log-file" value="{3}"/>
    <property name="string-encryption" value="disable"/>
    <property name="control-flow-obfuscation" value="enable"/>
    <property name="extensive-flow-obfuscation" value="maximum"/>
    <property name="skip-renaming" value="disable"/>
    <property name="member-reorder" value="enable"/>
</config>
	'''.format(inJar, outJar, androidJar, log) 
	
	f = open(output, 'w')
	f.write(configContent)
	f.close()
	print ('configuration file can be found at '+output)

#control flow + reorder members + string encryption
def create_cf_rm_sencryption_config(inJar, outJar, androidJar, log, output):
	configContent = '''
	<config>
    <input>
        <jar in="{0}" out="{1}"/>
    </input>
    <classpath>
        <jar name="{2}"/>
    </classpath>

	<keep-names>
		<class access="private+" stop="yes">
		<field access="private+"/>
		<method access="private+"/>
		</class>
	</keep-names>

    <property name="log-file" value="{3}"/>
    <property name="string-encryption" value="enable"/>
    <property name="string-encryption-type" value="strong"/>
    <property name="control-flow-obfuscation" value="enable"/>
    <property name="extensive-flow-obfuscation" value="maximum"/>
    <property name="skip-renaming" value="enable"/>
    <property name="member-reorder" value="enable"/>
</config>
	'''.format(inJar, outJar, androidJar, log) 
	
	f = open(output, 'w')
	f.write(configContent)
	f.close()
	print ('configuration file can be found at '+output)
	
# All: Control Flow + Reorder Member + renaming + String Encryption  obfuscation	
def create_all_config(inJar, outJar, androidJar, log, output):
	configContent = '''
	<config>
    <input>
        <jar in="{0}" out="{1}"/>
    </input>
    <classpath>
        <jar name="{2}"/>
    </classpath>

	<keep-names>
		<class access="public">
		<field access="public"/>
		<method access="public"/>
		</class>
	</keep-names>

    <property name="log-file" value="{3}"/>
    <property name="string-encryption" value="enable"/>
    <property name="string-encryption-type" value="strong"/>
    <property name="control-flow-obfuscation" value="enable"/>
    <property name="extensive-flow-obfuscation" value="maximum"/>
    <property name="skip-renaming" value="disable"/>
    <property name="member-reorder" value="enable"/>
</config>
	'''.format(inJar, outJar, androidJar, log) 
	
	f = open(output, 'w')
	f.write(configContent)
	f.close()
	print ('configuration file can be found at '+output)
	
