MANIFEST = {
	"NPC" : {
		"sighted": [
			"An NPC is within detectable range of the player. ", "You can be seen by someone. "
		]
	},
	"towns" : {
		"core" : {
			"landlocked" : [ "Fort ", "" ]
		},
		"blocks": {
			"1": ["Slon", "Flon", "Ren", "Fen"],
			"2": ["fin", "gon", "gen"],
			"3": ["borough", "burg", "ly", "gly", "ton", "ness"],
		}
	},
	"olds" : {
		"towns": {
			"landlocked" : [ "Fort <%olds.start%>", "Mount <%olds.start%>", "<%olds.start%> Gate", "<%olds.start%>" ],
			"seaside" : [ "Port <%olds.start%>", "<%olds.start%> Dock" ],
			"oceanic" : [ "<%olds.start%>", "<%olds.start%>" ]
		},
		
		"town" : {
			"pre": [
				"High ", "Low ", "<%olds.positionals%> ", ""
			],
			"core" : [
				"fart", "wang", "Slon", "Covid", "Butt", "dive", "fenn", "mole", "fingley", "Ten", "Net", "Fet"
			],
			"posts": [
				"<%olds.town.post%><%olds.posts%>", "<%oldstown.post%>",
				
			],
			"post" : [
				"ville", "ton", "hole", "wood", "borough"
			]
		},
		"more_positionals" : {
			"based" : [
				"over", "under", "juxta", "tween"
			]
		},
		"positionals" : [
			"Upper", "Lower"
		],

		"start" : [
			"<%olds.town.pre%><%olds.town.core%><%olds.town.post%><%olds.posts%>",
			"<%olds.town2.exec%>",
		],
		"space": [ "", "-", " " ],
		"town2" : {
			"begin" : [ "", "Upper ", "Lower ", "Inner ", "Outer " ],
			"core1" : [ "Ren", "Ten", "Twin", "Twig", "Hex", "Fox", "Pas", "San", "Sand", "Mer", "Rin", "Crop", "Mil", "Milk", "Otter"],
			"core2" : [ "fell", "all", "gle", "gen", "gon", "fall", "nell", "nal", "try", "wick", "wich", "maid", "well", "wall"],
			"exec": [ "<%olds.town2.begin%><%olds.town2.core1%><%olds.town2.core2%>" ]
		},
		"posts" : [
			"-on-sea", " by <%olds.town2.exec%>", " <%olds.more_positionals.based%> <%olds.town2.exec%>"
		],



	}
}