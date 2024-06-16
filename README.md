# answer = self.graph.run("MATCH (p1 {title:\"" + str(entity1) + "\"}),(p2{title:\"" + str(
        #     entity2) + "\"}),p=shortestpath((p1)-[*..10]-(p2)) RETURN p").evaluate()