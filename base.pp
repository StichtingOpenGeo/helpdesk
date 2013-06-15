class django {
	package {
		["python", "python-pip", "python-dev", "postgresql-server-dev-all", "screen", "gettext", "texlive"] : ensure => installed
	}

	package { ["django==1.5", "psycopg2==2.4.5", "south"]:
		ensure => installed,
		provider => pip,
	}

	class { 'postgresql::server':
	    config_hash => {
		'ip_mask_deny_postgres_user' => '0.0.0.0/32',
		'ip_mask_allow_all_users'    => '0.0.0.0/0',
		'listen_addresses'           => '*',
		'postgres_password'          => 'postgres',
	    },
	}

	postgresql::database{ 'openov_helpdesk':
	  charset => 'utf8',
	  require => Class['postgresql::server'],
	}

  postgresql::database{ 'test_openov_helpdesk':
	  charset => 'utf8',
	  require => Class['postgresql::server'],
	}

	postgresql::database_user{ 'openov_helpdesk':
	  password_hash => postgresql_password('openov_helpdesk', 'openov_helpdesk'),
	  require       => Class['postgresql::server'],
	}

	postgresql::database_grant{'openov_helpdesk':
	    privilege   => 'ALL',
	    db          => 'openov_helpdesk',
	    role        => 'openov_helpdesk',
	}

  postgresql::database_grant{'test_openov_helpdesk':
	    privilege   => 'ALL',
	    db          => 'test_openov_helpdesk',
	    role        => 'openov_helpdesk',
	}
}

include django

