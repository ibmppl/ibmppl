import time
from py_shell_wrapper import *;
######################################################################
######################################################################
def benchmark_read(num_v):
   #glib.test_graph(num_v);
   #return;
   start_time = time.time();
   g = Graph("database", "benchmark");
   create_time = time.time();
   labels=["label0","label1","label2","label3"];
   lab_0 = g.get_or_allocate_labelid(labels[0]);
   lab_1 = g.get_or_allocate_labelid(labels[1]);
   lab_2 = g.get_or_allocate_labelid(labels[2]);
   my_queue=[];
   for i in range (0, num_v):
      src_lab ="VertexLab%d"%i
      src_v = g.find_vertex("name",src_lab);
      src_val = src_v.get_subproperty("name");
      if not (src_lab == src_val.c_ptr.value):
         fail_counter+=1;
      for e1 in src_v.edges_label(lab_0):
         nbr_1 = g.find_vertex_vid(e1.target());
         for e2 in nbr_1.edges_label(lab_1):
            nbr_2=g.find_vertex_vid(e2.target());
            for e3 in nbr_2.edges_label(lab_2):
               nbr_3=g.find_vertex_vid(e3.target());
               my_queue.append(nbr_3);
       #TODO Implement map from labels to vertex.
   traversal_3_time = time.time();
   my_queue=[]
   for i in range (0, num_v):
      src_lab ="VertexLab%d"%i
      src_v = g.find_vertex("name",src_lab);
      src_val = src_v.get_subproperty("name");
      if not (src_lab == src_val.c_ptr.value):
         fail_counter+=1;
      for e1 in src_v.edges_label(lab_0):
         nbr_1 = g.find_vertex_vid(e1.target());
         for e2 in nbr_1.edges_label(lab_1):
            nbr_2=g.find_vertex_vid(e2.target());
            for e3 in nbr_2.edges_label(lab_2):
               nbr_3=g.find_vertex_vid(e3.target());
               my_queue.append(nbr_3);
       #TODO Implement map from labels to vertex.
   traversal_3_2_time = time.time();
   print "--Open: %6.6g"%(create_time-start_time);
   print "--Traversal3 : %6.6g"%(traversal_3_time - create_time);
   print "--Traversal3_2 : %6.6g"%(traversal_3_2_time - traversal_3_time);



def benchmark(num_v , num_e ):
   start_time = time.time();
   g = Graph("database", "benchmark");
   create_time = time.time();
   g.add_index("name", True);
   add_index_time = time.time();
   for i in range(0, num_v):
      vert = g.add_vertex(i%4);
      vert_f = g.find_vertex_vid(i%4);
      v_lab = "VertexLab%d"%i
      vert.set_subproperty("name", v_lab);
   add_vertex_time=time.time();
   print "Done adding vertices\n"
   fail_counter=0;
   for i in range(0,num_v):
      v_lab = "VertexLab%d"%i
      vert_f=g.find_vertex("name",v_lab);
      v_lab_f = vert_f.get_subproperty("name");
      if not(v_lab == v_lab_f.c_ptr.value):
         fail_counter+=1;
   vertex_find_time = time.time();
   print "Failed : %d \n"%fail_counter
   labels=["label0","label1","label2","label3"];
   for i in range (0,num_e):
      src = randint(0, num_v-1);
      dst = randint(0, num_v-1);
      src_lab="VertexLab%d"%src
      dst_lab="VertexLab%d"%dst
      edge = g.add_edge("name",src_lab, dst_lab,labels[i%4]);
      edge.set_subproperty("name", "Jill");
   add_edge_time = time.time();
   lab_0 = g.get_or_allocate_labelid(labels[0]);
   lab_1 = g.get_or_allocate_labelid(labels[1]);
   lab_2 = g.get_or_allocate_labelid(labels[2]);
   my_queue=[];
   for i in range (0, num_v):
      src_lab ="VertexLab%d"%i
      src_v = g.find_vertex("name",src_lab);
      src_val = src_v.get_subproperty("name");
      if not (src_lab == src_val.c_ptr.value):
         fail_counter+=1;
      for e1 in src_v.edges_label(lab_0):
         nbr_1 = g.find_vertex_vid(e1.target());
         for e2 in nbr_1.edges_label(lab_1):
            nbr_2=g.find_vertex_vid(e2.target());
            for e3 in nbr_2.edges_label(lab_2):
               nbr_3=g.find_vertex_vid(e3.target());
               my_queue.append(nbr_3);
       #TODO Implement map from labels to vertex.
   traversal_3_time = time.time();
   e_counter = 0;
   pred = 0;
   for v in g.vertices():
      for lab in [lab_0, lab_1, lab_2]:
         for e in v.edges_label(lab):
            e_counter+=1;
         for p in v.predecessors_label(lab):
            pred+=1;
   traversal_1_time = time.time();
   print "Failed : %d\n"%fail_counter
   print "Create : %6.6g"%(create_time-start_time);
   print "AddIndex: %6.6g"%(add_index_time-create_time );
   print "AddVertex: %6.6g"%(add_vertex_time -add_index_time);
   print "FindVertex: %6.6g"%(vertex_find_time - add_vertex_time );
   print "AddEdge: %6.6g"%(add_edge_time - vertex_find_time );
   print "Traversal3 : %6.6g"%(traversal_3_time - add_edge_time );
   print "Traversal1 : %6.6g"%(traversal_1_time - traversal_3_time );
   #g.print_graph()

def main():
   benchmark(100,1000);
   benchmark_read(100);
   if(True):
      return
   g = Graph("database", "dgraph");
   print ('Created graph ', g.g);
   g.load_csv_vertices("test_vertices.csv", True, ",",0," ",2);
   g.load_csv_edges("test_edges.csv", True,",", 0,1, "EDGE",0);
   g.create_random(1000,4000);
   g.add_vertex(1);
   g.add_vertex(2);
   g.add_vertex(3);
   g.add_vertex(4);
   g.add_vertex(5);

   g.print_graph();
   for v in g.vertices():
      print ('Vertex ', v.id())
      for p in v.properties():
         print ('Prop ', p.name(), p.value());
      for pred in v.predecessors():
         print ('Pred: ', pred.edge_id(), pred.vertex_id() );
      for e in v.edges():
         print ('Edge ', e.target())
         for pe in e.properties():
            print ('E-Prop ', pe.name(), pe.value())

if __name__ =="__main__":
   main();
