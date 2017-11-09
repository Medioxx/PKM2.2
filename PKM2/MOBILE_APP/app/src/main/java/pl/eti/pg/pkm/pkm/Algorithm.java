package pl.eti.pg.pkm.pkm;

/**
 * Created by EO NETWORKS on 07.11.2017.
 */

public class Algorithm {
    String name = null;
    boolean selected = false;

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

    public boolean isSelected() {
        return selected;
    }

    public void setSelected(boolean selected) {
        this.selected = selected;
    }
}
