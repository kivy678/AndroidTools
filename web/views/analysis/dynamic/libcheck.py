# -*- coding:utf-8 -*-

################################################################################

from flask.views import MethodView
from flask import render_template, request

from werkzeug.utils import secure_filename
from web.views.analysis import view_dynamic

from module.mobile.DeviceManager.process import ProcessInfor
from module.mobile.Analysis.dynamic.mview import getMemory
from module.mobile.Analysis.static.create_lib import createLibrary

from web.session import getSession
from module.mobile.cmd import shell

from util.fsUtils import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

import elfformat

import networkx as nx

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import random

################################################################################

sp              = getSharedPreferences(SHARED_PATH)
DATA_DIR        = sp.getString('DATA_DIR')

MEM_FILTER      = ['/data/data/', '/data/app/', 'libc.so']
filterName      = ['_']

################################################################################

class LIB_CHECK(MethodView):
    template_name = None

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        pkg = getSession('pkg')
        pid_list = self.getPid(pkg)

        if pid_list is None:
            return "앱을 실행하세요"

        data = list()
        for pid in pid_list:
            data.append((pid, iter(getMemory(pid, MEM_FILTER))))

        return render_template(self.template_name, enter=data)


    def post(self):
        if request.method == "POST":
            pid             = request.form.get("pid")
            start_addr      = request.form.get("GetStartAddr")
            end_addr        = request.form.get("GetEndAddr")
            lib_name        = request.form.get("GetLibName")

            if (start_addr is '') or (end_addr is ''):
                return "시작주소와 끝주소를 입력해주세요."

            f = request.files.get('SoFileName')
            fileName = f.filename

            org_path = Join(DATA_DIR, secure_filename(fileName))
            f.save(org_path)

            cmd = f"/data/local/tmp/MemoryDumper {pid} {start_addr} {end_addr}"
            shell.runCommand(cmd, shell=True, encoder='unicode-escape')

            cmd = f"adb pull /data/local/tmp/dump.bin {DATA_DIR}"
            shell.runCommand(cmd, shell=False)

            save_path = createLibrary(org_path, Join(DATA_DIR, "dump.bin"))

            mem = getMemory(int(pid))

            G = nx.Graph()
            for i in elfformat.GetGot(save_path).rstrip().split('\n'):
                lib = i.rstrip().split(' ')
                libAddr = int(lib[0], 16)

                try:
                    libName = lib[1]
                except IndexError:
                    libName = hex(libAddr)

                try:
                    for i in filterName:
                        if libName.startswith(i):
                            raise
                except:
                    continue


                for j in iter(mem):
                    str_addr = int(j.start_addr, 16)
                    end_addr = int(j.end_addr, 16)
                    shared_name = j.sharedName if j.sharedName != '' else hex(str_addr)

                    if str_addr < libAddr < end_addr:
                        #print(hex(str_addr),  hex(libAddr), hex(end_addr), shared_name, libName)
                        G.add_nodes_from([(shared_name, {'pos': [random.gauss(5, 3), random.gauss(5, 3)]})])
                        G.add_nodes_from([(libName,     {'pos': [random.gauss(5, 3), random.gauss(5, 3)]})])

                        G.add_edge(shared_name, libName)
                        break


            edge_x = []
            edge_y = []

            for edge in G.edges():
                x0, y0 = G.nodes[edge[0]]['pos']
                x1, y1 = G.nodes[edge[1]]['pos']
                edge_x.append(x0)
                edge_x.append(x1)
                edge_y.append(y0)
                edge_y.append(y1)

            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                mode='lines')

            node_x = []
            node_y = []
            for node in G.nodes():
                x, y = G.nodes[node]['pos']
                node_x.append(x)
                node_y.append(y)

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    showscale=True,
                    # colorscale options
                    #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                    #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                    #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                    colorscale='YlGnBu',
                    reversescale=True,
                    color=[],
                    size=10,
                    colorbar=dict(
                        thickness=15,
                        title='Call Count',
                        xanchor='left',
                        titleside='right'
                    ),
                    line_width=2))


            node_adjacencies = []
            node_text = []
            for adjacencies in G.adjacency():
                if len(adjacencies[1]) > 1:
                    node_adjacencies.append(255)
                else:
                    node_adjacencies.append(1)

                node_text.append(f"{adjacencies[0]}, call:{len(adjacencies[1])}")


            node_trace.marker.color = node_adjacencies
            node_trace.text = node_text


            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                            title="Library Call",
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Line",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002 ) ],
                            xaxis=dict(showgrid=True, zeroline=False, showticklabels=True),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                            )

            fig.show()

            #nx.draw(G, with_labels=True)
            #plt.show()
            #plt.close()

            return "완료"


    def getPid(self, pkg):
        pi = ProcessInfor()
        pid_list = pi.getPid(pkg)

        return pid_list


libcheck = LIB_CHECK.as_view('libcheck', template_name='analysis/dynamic/libcheck.jinja')
view_dynamic.add_url_rule('libcheck', view_func=libcheck)
