/**
 * Created by michellesun on 4/30/17.
 */


import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.firefox.internal.ProfilesIni;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;
import static org.junit.Assert.assertEquals;

public class APTTesting {
    private static WebDriver wd;
    private WebElement we;
    private WebElement result;
    private String output;
    @BeforeClass public static void setup() {
        ProfilesIni ini = new ProfilesIni();
        FirefoxProfile myprofile = ini.getProfile("Testing");
        wd = new FirefoxDriver(myprofile);
        // wd.get("https://advanced-programming-tools.appspot.com/");
        wd.get("http://localhost:8080/");

//        wd.get("file:///Users/michellesun/Desktop/files-for-ps6/pset6/minandmax.html");
    }
    @Test public void t0() {
        wd.navigate().refresh();
        we = wd.findElement(By.id("firstpage"));
        we.click();
        try {
            Thread.sleep(4000);

        } catch (Exception e) {
            e.printStackTrace();
        }
        we = wd.findElement(By.id("submit-login"));
        we.click();

        try {
            Thread.sleep(4000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("logoutId"));
        we.click();

        try {
            Thread.sleep(4000);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Test public void t1() {
        wd.navigate().refresh();
        we = wd.findElement(By.id("firstpage"));
        we.click();
        try {
            Thread.sleep(1000);

        } catch (Exception e) {
            e.printStackTrace();
        }
        we = wd.findElement(By.id("submit-login"));
        we.click();
        try {
            Thread.sleep(1000);

        } catch (Exception e) {
            e.printStackTrace();
        }
        we = wd.findElement(By.id("createId"));
        we.click();
        try {
            Thread.sleep(4000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("streamNameId"));
        we.sendKeys("Cat");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("coverId"));
        we.sendKeys("http://i4.buimg.com/567571/e0717fa9fa26c6f3.png\n");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("createButtonId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("viewId"));
        we.click();




        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("0"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("addFileId"));



        we.sendKeys("/Users/michellesun/Desktop/testPhotos/cat/Optimized-cat2.png");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("uploadStartButton"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        wd.navigate().refresh();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("logoutId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }


    }


    @Test public void t2() {
        wd.navigate().refresh();
        we = wd.findElement(By.id("firstpage"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }
        we = wd.findElement(By.id("submit-login"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("createId"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("streamNameId"));
        we.sendKeys("Beauty_and_Beast");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("tagId"));
        we.sendKeys("#Emma Watson");
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we.sendKeys("  #Film");




        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("coverId"));
        we.sendKeys("http://i2.muimg.com/567571/745d3b7789ec230c.png\n");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("createButtonId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("viewId"));
        we.click();




        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("1"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("addFileId"));



        we.sendKeys("/Users/michellesun/Desktop/testPhotos/beauty/Optimized-beauty2.png");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("addFileId"));

        we.sendKeys("/Users/michellesun/Desktop/testPhotos/beauty/Optimized-beauty3.png");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("addFileId"));

        we.sendKeys("/Users/michellesun/Desktop/testPhotos/beauty/Optimized-beauty4.png");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("addFileId"));

        we.sendKeys("/Users/michellesun/Desktop/testPhotos/beauty/Optimized-beauty5.png");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }



        we = wd.findElement(By.id("startUploadId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        wd.navigate().refresh();


        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("logoutId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

    }



    @Test public void t3() {
        wd.navigate().refresh();
        we = wd.findElement(By.id("firstpage"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }
        we = wd.findElement(By.id("submit-login"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("searchId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("query"));
        we.sendKeys("Cat");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("searchStartId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("logoutId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }


    }




    @Test public void t4() {
        wd.navigate().refresh();
        we = wd.findElement(By.id("firstpage"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("email"));
        we.clear();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we.sendKeys("testing2@gmail.com");

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("submit-login"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("trendingId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("0"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("subscr_stage_btn"));
        we.click();


        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("managementId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }


        we = wd.findElement(By.id("logoutId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    @Test public void t5() {
        wd.navigate().refresh();
        we = wd.findElement(By.id("firstpage"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }
        we = wd.findElement(By.id("submit-login"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }


        String[] streamName = new String[]{"Sunset", "Emma_Stone", "Transformers"};
        String[] coverId = new String[]{"http://i2.muimg.com/567571/4363223ba0b874e9.png\n", "http://i2.muimg.com/567571/e7b42821a71337c3.png\n", "http://i4.buimg.com/567571/6ab9ecd0e49e0baf.png\n"};

        List<List<String>> address = new ArrayList<>();
        List<String> sunsetAddress = new ArrayList<>(Arrays.asList("/Users/michellesun/Desktop/testPhotos/sunset/Optimized-sunset2.png", "/Users/michellesun/Desktop/testPhotos/sunset/Optimized-sunset3.png"));
        List<String> emmaAddress = new ArrayList<>(Arrays.asList("/Users/michellesun/Desktop/testPhotos/stone/Optimized-stone2.png"));
        List<String> transAddress = new ArrayList<>(Arrays.asList("/Users/michellesun/Desktop/testPhotos/trans/Optimized-trans2.png", "/Users/michellesun/Desktop/testPhotos/trans/Optimized-trans3.png", "/Users/michellesun/Desktop/testPhotos/trans/Optimized-trans4.png"));
        address.add(sunsetAddress);
        address.add(emmaAddress);
        address.add(transAddress);

        for(int i = 0; i < 3; i++){
            we = wd.findElement(By.id("createId"));
            we.click();
            try {
                Thread.sleep(2000);

            } catch (Exception e) {
                e.printStackTrace();
            }

            we = wd.findElement(By.id("streamNameId"));
            we.sendKeys(streamName[i]);

            try {
                Thread.sleep(2000);

            } catch (Exception e) {
                e.printStackTrace();
            }

            we = wd.findElement(By.id("coverId"));
            we.sendKeys(coverId[i]);
            try {
                Thread.sleep(2000);

            } catch (Exception e) {
                e.printStackTrace();
            }

            we = wd.findElement(By.id("createButtonId"));
            we.click();

            try {
                Thread.sleep(2000);

            } catch (Exception e) {
                e.printStackTrace();
            }

            we = wd.findElement(By.id("viewId"));
            we.click();




            try {
                Thread.sleep(2000);

            } catch (Exception e) {
                e.printStackTrace();
            }


            we = wd.findElement(By.id(new String(i + 2 + "")));
            we.click();


            for(int j = 0; j < address.get(i).size(); j++){
                try {
                    Thread.sleep(2000);

                } catch (Exception e) {
                    e.printStackTrace();
                }

                we = wd.findElement(By.id("addFileId"));

                List<String> cur = address.get(i);
                we.sendKeys(cur.get(j));

                try {
                    Thread.sleep(2000);

                } catch (Exception e) {
                    e.printStackTrace();
                }


            }

            try {
                Thread.sleep(2000);

            } catch (Exception e) {
                e.printStackTrace();
            }



            we = wd.findElement(By.id("startUploadId"));
            we.click();

            try {
                Thread.sleep(2000);

            } catch (Exception e) {
                e.printStackTrace();
            }

            wd.navigate().refresh();


        }



        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        wd.navigate().refresh();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("managementId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }



        we = wd.findElement(By.id("logoutId"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }


    }

    @Test public void t6() {
        wd.navigate().refresh();
        we = wd.findElement(By.id("firstpage"));
        we.click();
        try {
            Thread.sleep(1000);

        } catch (Exception e) {
            e.printStackTrace();
        }
        we = wd.findElement(By.id("submit-login"));
        we.click();
        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("0"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }

        we = wd.findElement(By.id("remove"));
        we.click();

        try {
            Thread.sleep(2000);

        } catch (Exception e) {
            e.printStackTrace();
        }





    }




}
