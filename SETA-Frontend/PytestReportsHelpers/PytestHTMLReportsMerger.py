from junitparser import JUnitXml

# TODO: package and release to public
'''
This is a custom class built to merge different HTML reports created by pytest-html into one report
'''


class HTMLMerger:
    def __init__(self, *args):
        self.files_path = args
        self.files_contents = list()
        self.headers = list()
        self.environment = list()
        self.summaries = list()
        self.results = list()
        self.errors = list()
        self.read_files_contents()
        self.extract_headers()
        self.extract_environments()
        self.extract_summary()
        self.extract_results()
        self.html_template = None

    def read_files_contents(self):
        for file in self.files_path:
            try:
                with open(file, 'r') as file_object:
                    self.files_contents.append(file_object.readlines())
            except FileNotFoundError as e:
                self.errors.append(e)

    def extract_headers(self):
        for file_content in self.files_contents:
            start = None
            end = None
            for line in file_content:
                if '<h1>' in line:
                    start = file_content.index(line)
                if '<h2>Environment' in line:
                    end = file_content.index(line)
                    header = file_content[start:end]
                    self.headers.append(header)
                    break

    def extract_environments(self):
        for file_content in self.files_contents:
            start = None
            end = None
            for line in file_content:
                if '<h2>Environment' in line:
                    start = file_content.index(line)
                if '<h2>Summary' in line:
                    end = file_content.index(line)
                    env = file_content[start:end]
                    self.environment.append(env)
                    break

    def extract_summary(self):
        for file_content in self.files_contents:
            start = None
            end = None
            for line in file_content:
                if '<h2>Summary' in line:
                    start = file_content.index(line)
                if '<h2>Results' in line:
                    end = file_content.index(line)
                    summary = file_content[start:end]
                    self.summaries.append(summary)
                    break

    def extract_results(self):
        for file_content in self.files_contents:
            start = None
            for line in file_content:
                if '<h2>Results' in line:
                    start = file_content.index(line)
                    result = file_content[start:]
                    result.pop()
                    result.append('</div></td></tr></tbody></table>')
                    self.results.append(result)
                    break

    def _create_html_template(self):
        self.html_template = ['<!DOCTYPE html>\n', '<html>\n', '   <head>\n', '      <meta charset="utf-8"/>\n',
                              '      <title>Test Report</title>\n', '      <style>body {\n',
                              '         font-family: Helvetica, Arial, sans-serif;\n', '         font-size: 12px;\n',
                              '         min-width: 1200px;\n', '         color: #999;\n', '         }\n',
                              '         h1 {\n', '         font-size: 24px;\n', '         color: black;\n',
                              '         }\n', '         h2 {\n', '         font-size: 16px;\n',
                              '         color: black;\n', '         }\n', '         p {\n', '         color: black;\n',
                              '         }\n', '         a {\n', '         color: #999;\n', '         }\n',
                              '         table {\n', '         border-collapse: collapse;\n', '         }\n',
                              '         /******************************\n', '         * SUMMARY INFORMATION\n',
                              '         ******************************/\n', '         #environment td {\n',
                              '         padding: 5px;\n', '         border: 1px solid #E6E6E6;\n', '         }\n',
                              '         #environment tr:nth-child(odd) {\n', '         background-color: #f6f6f6;\n',
                              '         }\n', '         /******************************\n',
                              '         * TEST RESULT COLORS\n', '         ******************************/\n',
                              '         span.passed, .passed .col-result {\n', '         color: green;\n',
                              '         }\n',
                              '         span.skipped, span.xfailed, span.rerun, .skipped .col-result, .xfailed .col-result, .rerun .col-result {\n',
                              '         color: orange;\n', '         }\n',
                              '         span.error, span.failed, span.xpassed, .error .col-result, .failed .col-result, .xpassed .col-result  {\n',
                              '         color: red;\n', '         }\n', '         /******************************\n',
                              '         * RESULTS TABLE\n', '         *\n', '         * 1. Table Layout\n',
                              '         * 2. Extra\n', '         * 3. Sorting items\n', '         *\n',
                              '         ******************************/\n', '         /*------------------\n',
                              '         * 1. Table Layout\n', '         *------------------*/\n',
                              '         #results-table {\n', '         border: 1px solid #e6e6e6;\n',
                              '         color: #999;\n', '         font-size: 12px;\n', '         width: 100%\n',
                              '         }\n', '         #results-table th, #results-table td {\n',
                              '         padding: 5px;\n', '         border: 1px solid #E6E6E6;\n',
                              '         text-align: left\n', '         }\n', '         #results-table th {\n',
                              '         font-weight: bold\n', '         }\n', '         /*------------------\n',
                              '         * 2. Extra\n', '         *------------------*/\n',
                              '         .log:only-child {\n', '         height: inherit\n', '         }\n',
                              '         .log {\n', '         background-color: #e6e6e6;\n',
                              '         border: 1px solid #e6e6e6;\n', '         color: black;\n',
                              '         display: block;\n',
                              '         font-family: "Courier New", Courier, monospace;\n', '         height: 230px;\n',
                              '         overflow-y: scroll;\n', '         padding: 5px;\n',
                              '         white-space: pre-wrap\n', '         }\n', '         div.image {\n',
                              '         border: 1px solid #e6e6e6;\n', '         float: right;\n',
                              '         height: 240px;\n', '         margin-left: 5px;\n',
                              '         overflow: hidden;\n', '         width: 320px\n', '         }\n',
                              '         div.image img {\n', '         width: 320px\n', '         }\n',
                              '         .collapsed {\n', '         display: none;\n', '         }\n',
                              '         .expander::after {\n', '         content: " (show details)";\n',
                              '         color: #BBB;\n', '         font-style: italic;\n',
                              '         cursor: pointer;\n', '         }\n', '         .collapser::after {\n',
                              '         content: " (hide details)";\n', '         color: #BBB;\n',
                              '         font-style: italic;\n', '         cursor: pointer;\n', '         }\n',
                              '         /*------------------\n', '         * 3. Sorting items\n',
                              '         *------------------*/\n', '         .sortable {\n',
                              '         cursor: pointer;\n', '         }\n', '         .sort-icon {\n',
                              '         font-size: 0px;\n', '         float: left;\n', '         margin-right: 5px;\n',
                              '         margin-top: 5px;\n', '         /*triangle*/\n', '         width: 0;\n',
                              '         height: 0;\n', '         border-left: 8px solid transparent;\n',
                              '         border-right: 8px solid transparent;\n', '         }\n',
                              '         .inactive .sort-icon {\n', '         /*finish triangle*/\n',
                              '         border-top: 8px solid #E6E6E6;\n', '         }\n',
                              '         .asc.active .sort-icon {\n', '         /*finish triangle*/\n',
                              '         border-bottom: 8px solid #999;\n', '         }\n',
                              '         .desc.active .sort-icon {\n', '         /*finish triangle*/\n',
                              '         border-top: 8px solid #999;\n', '         }\n', '      </style>\n',
                              '   </head>\n', '   <body onLoad="init()">\n',
                              '      <script>/* This Source Code Form is subject to the terms of the Mozilla Public\n',
                              '         * License, v. 2.0. If a copy of the MPL was not distributed with this file,\n',
                              '         * You can obtain one at http://mozilla.org/MPL/2.0/. */\n', '         \n',
                              '         \n', '         function toArray(iter) {\n',
                              '            if (iter === null) {\n', '                return null;\n', '            }\n',
                              '            return Array.prototype.slice.call(iter);\n', '         }\n', '         \n',
                              '         function find(selector, elem) {\n', '            if (!elem) {\n',
                              '                elem = document;\n', '            }\n',
                              '            return elem.querySelector(selector);\n', '         }\n', '         \n',
                              '         function find_all(selector, elem) {\n', '            if (!elem) {\n',
                              '                elem = document;\n', '            }\n',
                              '            return toArray(elem.querySelectorAll(selector));\n', '         }\n',
                              '         \n', '         function sort_column(elem) {\n',
                              '            toggle_sort_states(elem);\n',
                              '            var colIndex = toArray(elem.parentNode.childNodes).indexOf(elem);\n',
                              '            var key;\n', "            if (elem.classList.contains('numeric')) {\n",
                              '                key = key_num;\n',
                              "            } else if (elem.classList.contains('result')) {\n",
                              '                key = key_result;\n', '            } else {\n',
                              '                key = key_alpha;\n', '            }\n',
                              '            sort_table(elem, key(colIndex));\n', '         }\n', '         \n',
                              '         function show_all_extras() {\n',
                              "            find_all('.col-result').forEach(show_extras);\n", '         }\n',
                              '         \n', '         function hide_all_extras() {\n',
                              "            find_all('.col-result').forEach(hide_extras);\n", '         }\n',
                              '         \n', '         function show_extras(colresult_elem) {\n',
                              '            var extras = colresult_elem.parentNode.nextElementSibling;\n',
                              '            var expandcollapse = colresult_elem.firstElementChild;\n',
                              '            extras.classList.remove("collapsed");\n',
                              '            expandcollapse.classList.remove("expander");\n',
                              '            expandcollapse.classList.add("collapser");\n', '         }\n', '         \n',
                              '         function hide_extras(colresult_elem) {\n',
                              '            var extras = colresult_elem.parentNode.nextElementSibling;\n',
                              '            var expandcollapse = colresult_elem.firstElementChild;\n',
                              '            extras.classList.add("collapsed");\n',
                              '            expandcollapse.classList.remove("collapser");\n',
                              '            expandcollapse.classList.add("expander");\n', '         }\n', '         \n',
                              '         function show_filters() {\n',
                              "            var filter_items = document.getElementsByClassName('filter');\n",
                              '            for (var i = 0; i < filter_items.length; i++)\n',
                              '                filter_items[i].hidden = false;\n', '         }\n', '         \n',
                              '         function add_collapse() {\n', '            // Add links for show/hide all\n',
                              "            var resulttable = find('table#results-table');\n",
                              '            var showhideall = document.createElement("p");\n',
                              '            showhideall.innerHTML = \'<a href="javascript:show_all_extras()">Show all details</a> / \' +\n',
                              '                                    \'<a href="javascript:hide_all_extras()">Hide all details</a>\';\n',
                              '            resulttable.parentElement.insertBefore(showhideall, resulttable);\n',
                              '         \n', '            // Add show/hide link to each result\n',
                              "            find_all('.col-result').forEach(function(elem) {\n",
                              "                var collapsed = get_query_parameter('collapsed') || 'Passed';\n",
                              '                var extras = elem.parentNode.nextElementSibling;\n',
                              '                var expandcollapse = document.createElement("span");\n',
                              '                if (collapsed.includes(elem.innerHTML)) {\n',
                              '                    extras.classList.add("collapsed");\n',
                              '                    expandcollapse.classList.add("expander");\n',
                              '                } else {\n',
                              '                    expandcollapse.classList.add("collapser");\n', '                }\n',
                              '                elem.appendChild(expandcollapse);\n', '         \n',
                              '                elem.addEventListener("click", function(event) {\n',
                              '                    if (event.currentTarget.parentNode.nextElementSibling.classList.contains("collapsed")) {\n',
                              '                        show_extras(event.currentTarget);\n',
                              '                    } else {\n',
                              '                        hide_extras(event.currentTarget);\n', '                    }\n',
                              '                });\n', '            })\n', '         }\n', '         \n',
                              '         function get_query_parameter(name) {\n',
                              "            var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);\n",
                              "            return match && decodeURIComponent(match[1].replace(/\\+/g, ' '));\n",
                              '         }\n', '         \n', '         function init () {\n',
                              '            reset_sort_headers();\n', '         \n', '            add_collapse();\n',
                              '         \n', '            show_filters();\n', '         \n',
                              "            toggle_sort_states(find('.initial-sort'));\n", '         \n',
                              "            find_all('.sortable').forEach(function(elem) {\n",
                              '                elem.addEventListener("click",\n',
                              '                                      function(event) {\n',
                              '                                          sort_column(elem);\n',
                              '                                      }, false)\n', '            });\n', '         \n',
                              '         };\n', '         \n', '         function sort_table(clicked, key_func) {\n',
                              "            var rows = find_all('.results-table-row');\n",
                              "            var reversed = !clicked.classList.contains('asc');\n",
                              '            var sorted_rows = sort(rows, key_func, reversed);\n',
                              '            /* Whole table is removed here because browsers acts much slower\n',
                              '             * when appending existing elements.\n', '             */\n',
                              '            var thead = document.getElementById("results-table-head");\n',
                              "            document.getElementById('results-table').remove();\n",
                              '            var parent = document.createElement("table");\n',
                              '            parent.id = "results-table";\n', '            parent.appendChild(thead);\n',
                              '            sorted_rows.forEach(function(elem) {\n',
                              '                parent.appendChild(elem);\n', '            });\n',
                              '            document.getElementsByTagName("BODY")[0].appendChild(parent);\n',
                              '         }\n', '         \n', '         function sort(items, key_func, reversed) {\n',
                              '            var sort_array = items.map(function(item, i) {\n',
                              '                return [key_func(item), i];\n', '            });\n',
                              '            var multiplier = reversed ? -1 : 1;\n', '         \n',
                              '            sort_array.sort(function(a, b) {\n', '                var key_a = a[0];\n',
                              '                var key_b = b[0];\n',
                              '                return multiplier * (key_a >= key_b ? 1 : -1);\n', '            });\n',
                              '         \n', '            return sort_array.map(function(item) {\n',
                              '                var index = item[1];\n', '                return items[index];\n',
                              '            });\n', '         }\n', '         \n',
                              '         function key_alpha(col_index) {\n', '            return function(elem) {\n',
                              '                return elem.childNodes[1].childNodes[col_index].firstChild.data.toLowerCase();\n',
                              '            };\n', '         }\n', '         \n',
                              '         function key_num(col_index) {\n', '            return function(elem) {\n',
                              '                return parseFloat(elem.childNodes[1].childNodes[col_index].firstChild.data);\n',
                              '            };\n', '         }\n', '         \n',
                              '         function key_result(col_index) {\n', '            return function(elem) {\n',
                              "                var strings = ['Error', 'Failed', 'Rerun', 'XFailed', 'XPassed',\n",
                              "                               'Skipped', 'Passed'];\n",
                              '                return strings.indexOf(elem.childNodes[1].childNodes[col_index].firstChild.data);\n',
                              '            };\n', '         }\n', '         \n',
                              '         function reset_sort_headers() {\n',
                              "            find_all('.sort-icon').forEach(function(elem) {\n",
                              '                elem.parentNode.removeChild(elem);\n', '            });\n',
                              "            find_all('.sortable').forEach(function(elem) {\n",
                              '                var icon = document.createElement("div");\n',
                              '                icon.className = "sort-icon";\n',
                              '                icon.textContent = "vvv";\n',
                              '                elem.insertBefore(icon, elem.firstChild);\n',
                              '                elem.classList.remove("desc", "active");\n',
                              '                elem.classList.add("asc", "inactive");\n', '            });\n',
                              '         }\n', '         \n', '         function toggle_sort_states(elem) {\n',
                              '            //if active, toggle between asc and desc\n',
                              "            if (elem.classList.contains('active')) {\n",
                              "                elem.classList.toggle('asc');\n",
                              "                elem.classList.toggle('desc');\n", '            }\n', '         \n',
                              '            //if inactive, reset all other functions and add ascending active\n',
                              "            if (elem.classList.contains('inactive')) {\n",
                              '                reset_sort_headers();\n',
                              "                elem.classList.remove('inactive');\n",
                              "                elem.classList.add('active');\n", '            }\n', '         }\n',
                              '         \n', '         function is_all_rows_hidden(value) {\n',
                              '          return value.hidden == false;\n', '         }\n', '         \n',
                              '         function filter_table(elem) {\n',
                              '            var outcome_att = "data-test-result";\n',
                              '            var outcome = elem.getAttribute(outcome_att);\n',
                              '            class_outcome = outcome + " results-table-row";\n',
                              '            var outcome_rows = document.getElementsByClassName(class_outcome);\n',
                              '         \n', '            for(var i = 0; i < outcome_rows.length; i++){\n',
                              '                outcome_rows[i].hidden = !elem.checked;\n', '            }\n',
                              '         \n',
                              "            var rows = find_all('.results-table-row').filter(is_all_rows_hidden);\n",
                              '            var all_rows_hidden = rows.length == 0 ? true : false;\n',
                              '            var not_found_message = document.getElementById("not-found-message");\n',
                              '            not_found_message.hidden = !all_rows_hidden;\n', '         }\n',
                              '                \n', '      </script>\n', '      ']

    def create_merged_xml(self, report_name):
        self._create_html_template()
        for i in range(len(self.headers)):
            self.html_template.extend(self.headers[i])
            self.html_template.extend(self.environment[i])
            self.html_template.extend(self.summaries[i])
            self.html_template.extend(self.results[i])
        self.html_template.append('</body></html>')
        with open(report_name, 'w') as f:
            [f.write(line) for line in self.html_template]
            if self.errors:
                [f.write(str(e)) for e in self.errors]
        return


class XMLMerger:
    def __init__(self, *args):
        self.files_path = args
        self.xml_objects = list()
        self.errors = list()

    def _add_merged_files_to_list(self):
        try:
            for file_path in self.files_path:
                junit_obj = JUnitXml.fromfile(file_path)
                self.xml_objects.append(junit_obj)
        except FileNotFoundError as e:
            self.errors.append(e)

    def create_merged_html(self, report_name):
        merged_file = None
        for obj in self.xml_objects:
            merged_file += obj
        merged_file.write(report_name)
        if self.errors:
            merged_file.write([str(e) for e in self.errors])
