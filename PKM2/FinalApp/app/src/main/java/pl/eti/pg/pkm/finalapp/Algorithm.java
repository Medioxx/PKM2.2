package pl.eti.pg.pkm.finalapp;

/**
 * Created by EO NETWORKS on 03.12.2017.
 */

//klasa przechowująca informację o nazwie algorytmu oraz informację na temat wybrania algorytmu
public class Algorithm {
    String name = null;
    Boolean selected = false;

    public Algorithm(String name, Boolean selected) {
        this.name = name;
        this.selected = selected;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Boolean getSelected() {
        return selected;
    }

    public void setSelected(Boolean selected) {
        this.selected = selected;
    }
}
